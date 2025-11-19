'use client';

import { useState } from 'react';
import { Card, Title, Text } from '@tremor/react';
import UploadWizard from '@/components/upload/UploadWizard';

export default function UploadPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-8">
        <Title>Document Upload Pipeline</Title>
        <Text className="mt-2">
          Upload documents through our 5-step processing pipeline: Upload → Customer → Tags → Classify → Process
        </Text>
      </div>

      <UploadWizard />
    </div>
  );
}
