'use client';

import { useState } from 'react';
import { Card, Text, Button } from '@tremor/react';
import { Upload, X } from 'lucide-react';

interface FileUploadZoneProps {
  files: any[];
  onFilesChange: (files: any[]) => void;
}

export default function FileUploadZone({ files, onFilesChange }: FileUploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    await uploadFiles(droppedFiles);
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      await uploadFiles(selectedFiles);
    }
  };

  const uploadFiles = async (fileList: File[]) => {
    const formData = new FormData();
    fileList.forEach(file => formData.append('files', file));

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      if (data.success) {
        onFilesChange([...files, ...data.files]);
      }
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };

  const removeFile = (index: number) => {
    onFilesChange(files.filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-4">
      <div
        onDrop={handleDrop}
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        className={`border-2 border-dashed rounded-lg p-12 text-center transition ${
          isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
        }`}
      >
        <Upload className="mx-auto h-12 w-12 text-gray-400" />
        <Text className="mt-4">Drag files here or click to browse</Text>
        <input
          type="file"
          multiple
          onChange={handleFileSelect}
          className="hidden"
          id="file-upload"
          accept=".pdf,.doc,.docx,.txt,.md,.xls,.xlsx,.csv"
        />
        <label htmlFor="file-upload">
          <Button className="mt-4" as="span">Browse Files</Button>
        </label>
        <Text className="mt-2 text-sm text-gray-500">
          PDF, DOC, DOCX, TXT, MD, XLS, XLSX, CSV (max 100MB per file)
        </Text>
      </div>

      {files.length > 0 && (
        <Card>
          <Text className="font-semibold mb-2">Uploaded Files ({files.length})</Text>
          {files.map((file, idx) => (
            <div key={idx} className="flex justify-between items-center py-2 border-b">
              <div>
                <Text>{file.originalName}</Text>
                <Text className="text-sm text-gray-500">{(file.size / 1024 / 1024).toFixed(2)} MB</Text>
              </div>
              <Button size="xs" variant="light" onClick={() => removeFile(idx)}>
                <X className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </Card>
      )}
    </div>
  );
}
