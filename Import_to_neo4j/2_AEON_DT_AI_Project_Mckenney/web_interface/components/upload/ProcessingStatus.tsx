"use client";

import { useState, useEffect, useCallback } from "react";
import { Card, ProgressBar, Text, Badge } from "@tremor/react";

interface ProcessingStatusProps {
  jobIds: string[];
}

interface JobStatus {
  fileName: string;
  status: string;
  progress: number;
  message: string;
  steps: {
    classification: { status: string; progress: number };
    ner: { status: string; progress: number };
    ingestion: { status: string; progress: number };
  };
}

export default function ProcessingStatus({ jobIds }: ProcessingStatusProps) {
  const [jobs, setJobs] = useState<Map<string, JobStatus>>(new Map());
  const [errors, setErrors] = useState<Map<string, string>>(new Map());
  const [isPolling, setIsPolling] = useState(true);

  const fetchJobStatus = useCallback(async (jobId: string) => {
    try {
      const response = await fetch(`/api/pipeline/status/${jobId}`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      setJobs((prev) => {
        const updated = new Map(prev);
        updated.set(jobId, data);
        return updated;
      });
      
      setErrors((prev) => {
        const updated = new Map(prev);
        updated.delete(jobId);
        return updated;
      });
      
      return data;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Unknown error";
      
      setErrors((prev) => {
        const updated = new Map(prev);
        updated.set(jobId, errorMessage);
        return updated;
      });
      
      return null;
    }
  }, []);

  const pollAllJobs = useCallback(async () => {
    const statusPromises = jobIds.map(fetchJobStatus);
    const results = await Promise.all(statusPromises);
    
    const allComplete = results.every(
      (result) => result && result.status === "complete"
    );
    
    if (allComplete) {
      setIsPolling(false);
    }
  }, [jobIds, fetchJobStatus]);

  useEffect(() => {
    if (!isPolling || jobIds.length === 0) return;

    pollAllJobs();

    const intervalId = setInterval(() => {
      pollAllJobs();
    }, 2000);

    return () => clearInterval(intervalId);
  }, [jobIds, isPolling, pollAllJobs]);

  const getStatusColor = (status: string): "gray" | "blue" | "green" | "red" => {
    switch (status) {
      case "complete":
        return "green";
      case "processing":
        return "blue";
      case "failed":
        return "red";
      default:
        return "gray";
    }
  };

  const getStepLabel = (stepKey: string): string => {
    switch (stepKey) {
      case "classification":
        return "Classification";
      case "ner":
        return "Named Entity Recognition";
      case "ingestion":
        return "Ingestion";
      default:
        return stepKey;
    }
  };

  if (jobIds.length === 0) {
    return null;
  }

  return (
    <div className="space-y-4">
      <Text className="text-lg font-semibold">Processing Documents</Text>
      
      {jobIds.map((jobId) => {
        const job = jobs.get(jobId);
        const error = errors.get(jobId);

        if (error) {
          return (
            <Card key={jobId} className="border-red-200 bg-red-50">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Text className="font-medium">Job ID: {jobId}</Text>
                  <Badge color="red">Error</Badge>
                </div>
                <Text className="text-sm text-red-600">{error}</Text>
              </div>
            </Card>
          );
        }

        if (!job) {
          return (
            <Card key={jobId}>
              <div className="flex items-center justify-between">
                <Text className="font-medium">Job ID: {jobId}</Text>
                <Badge color="gray">Loading...</Badge>
              </div>
            </Card>
          );
        }

        return (
          <Card key={jobId}>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <Text className="font-bold">{job.fileName}</Text>
                <Badge color={getStatusColor(job.status)}>
                  {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
                </Badge>
              </div>

              <div className="space-y-1">
                <div className="flex items-center justify-between">
                  <Text className="text-sm">{job.message}</Text>
                  <Text className="text-sm font-medium">{job.progress}%</Text>
                </div>
                <ProgressBar value={job.progress} color={getStatusColor(job.status)} />
              </div>

              <div className="space-y-2 pt-2 border-t border-gray-200">
                {Object.entries(job.steps).map(([stepKey, stepData]) => (
                  <div key={stepKey} className="space-y-1">
                    <div className="flex items-center justify-between">
                      <Text className="text-xs text-gray-600">
                        {getStepLabel(stepKey)}
                      </Text>
                      <div className="flex items-center gap-2">
                        <Text className="text-xs">{stepData.progress}%</Text>
                        <Badge 
                          size="xs" 
                          color={getStatusColor(stepData.status)}
                        >
                          {stepData.status}
                        </Badge>
                      </div>
                    </div>
                    <ProgressBar 
                      value={stepData.progress} 
                      color={getStatusColor(stepData.status)}
                      className="h-1"
                    />
                  </div>
                ))}
              </div>
            </div>
          </Card>
        );
      })}
    </div>
  );
}
