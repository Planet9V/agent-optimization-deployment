import { useState, useCallback } from 'react';
import { Card, Text, Button, Badge, Flex } from '@tremor/react';
import { Upload, File, X, CheckCircle, AlertCircle } from 'lucide-react';

interface UploadedFile {
  id: string;
  file: File;
  status: 'pending' | 'uploading' | 'success' | 'error';
  progress?: number;
  error?: string;
}

interface FileUploadProps {
  onFilesSelected?: (files: File[]) => void;
  onUpload?: (files: File[]) => Promise<void>;
  acceptedFileTypes?: string[];
  maxFileSize?: number; // in MB
  maxFiles?: number;
  multiple?: boolean;
}

const defaultAcceptedTypes = [
  '.pdf', '.doc', '.docx', '.txt', '.md',
  '.xls', '.xlsx', '.csv',
  '.jpg', '.jpeg', '.png', '.gif'
];

export default function FileUpload({
  onFilesSelected,
  onUpload,
  acceptedFileTypes = defaultAcceptedTypes,
  maxFileSize = 50,
  maxFiles = 10,
  multiple = true
}: FileUploadProps) {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const validateFile = (file: File): string | undefined => {
    const extension = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!acceptedFileTypes.includes(extension)) {
      return `File type ${extension} is not supported`;
    }

    const fileSizeMB = file.size / (1024 * 1024);
    if (fileSizeMB > maxFileSize) {
      return `File size exceeds ${maxFileSize}MB limit`;
    }

    return undefined;
  };

  const handleFiles = (files: FileList | null) => {
    if (!files) return;

    const fileArray = Array.from(files);
    const newFiles: UploadedFile[] = [];

    fileArray.forEach((file) => {
      if (uploadedFiles.length + newFiles.length >= maxFiles) {
        return;
      }

      const error = validateFile(file);
      newFiles.push({
        id: `${Date.now()}-${Math.random()}`,
        file,
        status: error ? 'error' : 'pending',
        error
      });
    });

    setUploadedFiles(prev => [...prev, ...newFiles]);

    const validFiles = newFiles
      .filter(f => f.status === 'pending')
      .map(f => f.file);

    if (validFiles.length > 0 && onFilesSelected) {
      onFilesSelected(validFiles);
    }
  };

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    handleFiles(e.dataTransfer.files);
  }, [uploadedFiles.length]);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFiles(e.target.files);
    e.target.value = '';
  };

  const removeFile = (id: string) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== id));
  };

  const handleUpload = async () => {
    const filesToUpload = uploadedFiles
      .filter(f => f.status === 'pending')
      .map(f => f.file);

    if (filesToUpload.length === 0 || !onUpload) return;

    setIsUploading(true);
    try {
      await onUpload(filesToUpload);
      setUploadedFiles(prev =>
        prev.map(f =>
          f.status === 'pending' ? { ...f, status: 'success' } : f
        )
      );
    } catch (error) {
      console.error('Upload failed:', error);
      setUploadedFiles(prev =>
        prev.map(f =>
          f.status === 'pending'
            ? { ...f, status: 'error', error: 'Upload failed' }
            : f
        )
      );
    } finally {
      setIsUploading(false);
    }
  };

  const clearAll = () => {
    setUploadedFiles([]);
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  const pendingCount = uploadedFiles.filter(f => f.status === 'pending').length;
  const successCount = uploadedFiles.filter(f => f.status === 'success').length;
  const errorCount = uploadedFiles.filter(f => f.status === 'error').length;

  return (
    <Card>
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          isDragging
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
      >
        <Upload className={`h-12 w-12 mx-auto mb-4 ${
          isDragging ? 'text-blue-500' : 'text-gray-400'
        }`} />
        <Text className="text-lg font-semibold mb-2">
          {isDragging ? 'Drop files here' : 'Drag & drop files here'}
        </Text>
        <Text className="text-sm text-gray-500 mb-4">
          or click to browse (max {maxFileSize}MB per file, up to {maxFiles} files)
        </Text>

        <input
          type="file"
          id="file-input"
          className="hidden"
          onChange={handleFileInput}
          multiple={multiple}
          accept={acceptedFileTypes.join(',')}
          disabled={uploadedFiles.length >= maxFiles}
        />

        <Button
          onClick={() => document.getElementById('file-input')?.click()}
          icon={Upload}
          disabled={uploadedFiles.length >= maxFiles}
        >
          Select Files
        </Button>

        <Text className="text-xs text-gray-400 mt-4">
          Supported: {acceptedFileTypes.join(', ')}
        </Text>
      </div>

      {uploadedFiles.length > 0 && (
        <div className="mt-6">
          <Flex justifyContent="between" alignItems="center" className="mb-4">
            <Text className="font-semibold">
              Files ({uploadedFiles.length})
            </Text>
            <Flex justifyContent="end" className="space-x-2">
              {pendingCount > 0 && (
                <Badge color="blue">{pendingCount} pending</Badge>
              )}
              {successCount > 0 && (
                <Badge color="green">{successCount} uploaded</Badge>
              )}
              {errorCount > 0 && (
                <Badge color="red">{errorCount} failed</Badge>
              )}
            </Flex>
          </Flex>

          <div className="space-y-2 max-h-96 overflow-y-auto">
            {uploadedFiles.map((uploadedFile) => {
              const StatusIcon =
                uploadedFile.status === 'success' ? CheckCircle :
                uploadedFile.status === 'error' ? AlertCircle :
                File;

              const statusColor =
                uploadedFile.status === 'success' ? 'text-green-600' :
                uploadedFile.status === 'error' ? 'text-red-600' :
                'text-gray-400';

              return (
                <div
                  key={uploadedFile.id}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <Flex justifyContent="start" className="space-x-3 flex-1 min-w-0">
                    <StatusIcon className={`h-5 w-5 flex-shrink-0 ${statusColor}`} />
                    <div className="flex-1 min-w-0">
                      <Text className="font-medium truncate">
                        {uploadedFile.file.name}
                      </Text>
                      <Text className="text-xs text-gray-500">
                        {formatFileSize(uploadedFile.file.size)}
                      </Text>
                      {uploadedFile.error && (
                        <Text className="text-xs text-red-600 mt-1">
                          {uploadedFile.error}
                        </Text>
                      )}
                    </div>
                  </Flex>
                  <Button
                    size="xs"
                    variant="light"
                    color="red"
                    icon={X}
                    onClick={() => removeFile(uploadedFile.id)}
                    disabled={isUploading}
                  >
                    Remove
                  </Button>
                </div>
              );
            })}
          </div>

          <Flex justifyContent="end" className="space-x-2 mt-4">
            <Button
              variant="secondary"
              onClick={clearAll}
              disabled={isUploading}
            >
              Clear All
            </Button>
            {onUpload && pendingCount > 0 && (
              <Button
                icon={Upload}
                onClick={handleUpload}
                loading={isUploading}
                disabled={isUploading}
              >
                Upload {pendingCount} {pendingCount === 1 ? 'File' : 'Files'}
              </Button>
            )}
          </Flex>
        </div>
      )}
    </Card>
  );
}
