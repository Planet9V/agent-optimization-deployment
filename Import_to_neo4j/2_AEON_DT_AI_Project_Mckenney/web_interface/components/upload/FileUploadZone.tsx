"use client";

import React, { useCallback, useState } from "react";
import { Upload, X, AlertCircle } from "lucide-react";
import { Card, Text } from "@tremor/react";

interface UploadedFile {
  originalName: string;
  path: string;
  size: number;
  type: string;
}

interface FileUploadZoneProps {
  files: UploadedFile[];
  onFilesChange: (files: UploadedFile[]) => void;
}

const MAX_FILE_SIZE = 100 * 1024 * 1024; // 100MB
const MAX_FILES = 20;
const ALLOWED_TYPES = [
  "application/pdf",
  "application/msword",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "text/plain",
  "text/markdown",
  "application/vnd.ms-excel",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  "text/csv",
];

const ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx", ".txt", ".md", ".xls", ".xlsx", ".csv"];

export default function FileUploadZone({ files, onFilesChange }: FileUploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
  };

  const validateFile = (file: File): string | null => {
    // Check file size
    if (file.size > MAX_FILE_SIZE) {
      return `File "${file.name}" exceeds maximum size of 100MB`;
    }

    // Check file type
    const extension = "." + file.name.split(".").pop()?.toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(extension) && !ALLOWED_TYPES.includes(file.type)) {
      return `File "${file.name}" has an unsupported format. Allowed: PDF, DOC, DOCX, TXT, MD, XLS, XLSX, CSV`;
    }

    return null;
  };

  const uploadFiles = async (filesToUpload: File[]) => {
    // Validate total file count
    if (files.length + filesToUpload.length > MAX_FILES) {
      setError(`Cannot upload more than ${MAX_FILES} files total. Currently have ${files.length} files.`);
      return;
    }

    // Validate each file
    for (const file of filesToUpload) {
      const validationError = validateFile(file);
      if (validationError) {
        setError(validationError);
        return;
      }
    }

    setUploading(true);
    setError(null);

    try {
      const uploadedFiles: UploadedFile[] = [];

      for (const file of filesToUpload) {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("/api/upload", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || `Failed to upload ${file.name}`);
        }

        const result = await response.json();
        uploadedFiles.push({
          originalName: file.name,
          path: result.path,
          size: file.size,
          type: file.type,
        });
      }

      onFilesChange([...files, ...uploadedFiles]);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to upload files";
      setError(errorMessage);
      console.error("Upload error:", err);
    } finally {
      setUploading(false);
    }
  };

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);

      const droppedFiles = Array.from(e.dataTransfer.files);
      if (droppedFiles.length > 0) {
        uploadFiles(droppedFiles);
      }
    },
    [files, onFilesChange]
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFiles = e.target.files;
      if (selectedFiles && selectedFiles.length > 0) {
        uploadFiles(Array.from(selectedFiles));
      }
      // Reset input value to allow selecting the same file again
      e.target.value = "";
    },
    [files, onFilesChange]
  );

  const removeFile = (index: number) => {
    const updatedFiles = files.filter((_, i) => i !== index);
    onFilesChange(updatedFiles);
    setError(null);
  };

  return (
    <div className="w-full">
      {/* Error Display */}
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 flex-shrink-0" />
          <div>
            <p className="text-sm font-medium text-red-800">Upload Error</p>
            <p className="text-sm text-red-700 mt-1">{error}</p>
          </div>
          <button
            onClick={() => setError(null)}
            className="ml-auto text-red-600 hover:text-red-800"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      )}

      {/* Upload Zone */}
      <div
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`
          relative border-2 border-dashed rounded-lg p-8 text-center transition-colors cursor-pointer
          ${isDragging ? "border-blue-500 bg-blue-50" : "border-gray-300 bg-gray-50 hover:border-blue-400 hover:bg-blue-50"}
          ${uploading ? "opacity-50 cursor-not-allowed" : ""}
        `}
      >
        <input
          type="file"
          multiple
          accept={ALLOWED_EXTENSIONS.join(",")}
          onChange={handleFileInput}
          disabled={uploading}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
        />
        <Upload className={`mx-auto h-12 w-12 mb-4 ${isDragging ? "text-blue-500" : "text-gray-400"}`} />
        <Text className="text-lg font-medium mb-2">
          {uploading ? "Uploading..." : "Drag files or click to browse"}
        </Text>
        <Text className="text-sm text-gray-500">
          Supported: PDF, DOC, DOCX, TXT, MD, XLS, XLSX, CSV
        </Text>
        <Text className="text-sm text-gray-500 mt-1">
          Max {formatFileSize(MAX_FILE_SIZE)} per file, {MAX_FILES} files maximum
        </Text>
      </div>

      {/* Uploaded Files List */}
      {files.length > 0 && (
        <div className="mt-6">
          <Text className="font-medium mb-3">Uploaded Files ({files.length}/{MAX_FILES})</Text>
          <div className="space-y-2">
            {files.map((file, index) => (
              <Card key={index} className="p-3">
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <Text className="font-medium truncate">{file.originalName}</Text>
                    <Text className="text-sm text-gray-500">{formatFileSize(file.size)}</Text>
                  </div>
                  <button
                    onClick={() => removeFile(index)}
                    className="ml-4 p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Remove file"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
