'use client';

import { useState, useEffect } from 'react';
import { Card, Text, ProgressBar } from '@tremor/react';

interface Props {
  jobIds: string[];
}

export default function ProcessingStatus({ jobIds }: Props) {
  const [statuses, setStatuses] = useState<any[]>([]);

  useEffect(() => {
    const interval = setInterval(async () => {
      const results = await Promise.all(
        jobIds.map(id => fetch(`/api/pipeline/status/${id}`).then(r => r.json()))
      );
      setStatuses(results);

      if (results.every(r => r.status === 'complete')) {
        clearInterval(interval);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobIds]);

  return (
    <div className="space-y-4">
      {statuses.map((status, idx) => (
        <Card key={idx}>
          <Text className="font-semibold">{status.fileName || `File ${idx + 1}`}</Text>
          <Text className="text-sm text-gray-500 mt-1">{status.message}</Text>
          <ProgressBar value={status.progress || 0} className="mt-2" />
          <Text className="text-sm mt-1">{status.status}</Text>
        </Card>
      ))}
    </div>
  );
}
