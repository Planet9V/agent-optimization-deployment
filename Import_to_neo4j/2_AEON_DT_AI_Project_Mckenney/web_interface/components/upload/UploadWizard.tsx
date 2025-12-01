'use client';

import { useState } from 'react';
import { Card, Title, Text, Button, ProgressBar } from '@tremor/react';
import FileUploadZone from './FileUploadZone';
import CustomerSelector from './CustomerSelector';
import TagSelector from './TagSelector';
import SectorClassifier from './SectorClassifier';
import ProcessingStatus from './ProcessingStatus';

interface UploadedFile {
  originalName: string;
  path: string;
  size: number;
  type: string;
}

export default function UploadWizard() {
  const [currentStep, setCurrentStep] = useState(1);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [selectedCustomer, setSelectedCustomer] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [selectedSector, setSelectedSector] = useState('');
  const [selectedSubsector, setSelectedSubsector] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [jobIds, setJobIds] = useState<string[]>([]);

  const STEPS = ['Upload', 'Customer', 'Tags', 'Classify', 'Process'];

  const canProceed = () => {
    switch (currentStep) {
      case 1: return uploadedFiles.length > 0;
      case 2: return selectedCustomer !== '';
      case 3: return true;
      case 4: return selectedSector !== '';
      case 5: return false;
      default: return false;
    }
  };

  const handleNext = () => {
    if (currentStep < 5 && canProceed()) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    setIsProcessing(true);
    try {
      const response = await fetch('/api/pipeline/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          files: uploadedFiles,
          customer: selectedCustomer,
          tags: selectedTags,
          classification: { sector: selectedSector, subsector: selectedSubsector }
        })
      });
      const data = await response.json();
      if (data.success) {
        setJobIds(data.jobs.map((j: any) => j.jobId));
      }
    } catch (error) {
      console.error('Processing failed:', error);
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return <FileUploadZone files={uploadedFiles} onFilesChange={setUploadedFiles} />;
      case 2:
        return <CustomerSelector selected={selectedCustomer} onSelect={setSelectedCustomer} />;
      case 3:
        return <TagSelector selected={selectedTags} onChange={setSelectedTags} />;
      case 4:
        return <SectorClassifier 
          sector={selectedSector} 
          subsector={selectedSubsector}
          onSectorChange={setSelectedSector}
          onSubsectorChange={setSelectedSubsector}
        />;
      case 5:
        return jobIds.length > 0 ? (
          <ProcessingStatus jobIds={jobIds} />
        ) : (
          <div className="space-y-4">
            <Card>
              <Title>Ready to Process</Title>
              <div className="mt-4 space-y-2">
                <Text>Files: {uploadedFiles.length} documents</Text>
                <Text>Customer: {selectedCustomer}</Text>
                <Text>Tags: {selectedTags.join(', ' ) || 'None'}</Text>
                <Text>Classification: {selectedSector} {selectedSubsector && `→ ${selectedSubsector}`}</Text>
              </div>
              <Button className="mt-4" onClick={handleSubmit} disabled={isProcessing}>
                {isProcessing ? 'Processing...' : 'Start Processing'}
              </Button>
            </Card>
          </div>
        );
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-4">
        {STEPS.map((step, idx) => (
          <div key={idx} className="flex items-center">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
              idx + 1 === currentStep ? 'bg-blue-500 text-white' : 
              idx + 1 < currentStep ? 'bg-green-500 text-white' : 'bg-gray-300'
            }`}>
              {idx + 1}
            </div>
            <Text className="ml-2">{step}</Text>
          </div>
        ))}
      </div>

      <ProgressBar value={(currentStep / STEPS.length) * 100} className="mb-4" />

      <Card>
        <Title>Step {currentStep} of {STEPS.length}: {STEPS[currentStep - 1]}</Title>
        <div className="mt-6">
          {renderStep()}
        </div>

        <div className="flex justify-between mt-6">
          <Button onClick={handleBack} disabled={currentStep === 1} variant="secondary">
            Back
          </Button>
          {currentStep < 5 && (
            <Button onClick={handleNext} disabled={!canProceed()}>
              Next
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
}
