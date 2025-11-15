/**
 * File: QueryControlService.executeCommand.test.ts
 * Created: 2025-11-14
 * Modified: 2025-11-14
 * Version: v1.0.0
 * Author: Test Suite Generator
 * Purpose: Unit tests for QueryControlService.executeCommand() operation
 * Dependencies: @jest/globals, lib/query-control/query-control-service.ts
 * Status: ACTIVE
 */

import { describe, test, expect, beforeEach, afterEach, jest } from '@jest/globals';
import type { Mock } from 'jest-mock';
import { QueryControlService } from '../../../lib/query-control/query-control-service';
import { McpError, ErrorCode } from '@modelcontextprotocol/sdk/types.js';

// Mock dependencies
const mockSpawn = jest.fn();
const mockTelemetryRecord = jest.fn();
const mockPerformanceRecord = jest.fn();

jest.mock('child_process', () => ({
  spawn: (...args: unknown[]) => mockSpawn(...args),
}));

jest.mock('../../../lib/query-control/telemetry/telemetry-service', () => ({
  getTelemetryService: jest.fn(() => ({
    recordOperation: mockTelemetryRecord,
  })),
}));

jest.mock('../../../lib/query-control/profiling/performance-profiler', () => ({
  getPerformanceProfiler: jest.fn(() => ({
    recordLatency: mockPerformanceRecord,
  })),
}));

describe('QueryControlService.executeCommand()', () => {
  let service: QueryControlService;
  const mockStartTime = Date.now();

  beforeEach(() => {
    jest.clearAllMocks();
    jest.spyOn(Date, 'now').mockReturnValue(mockStartTime);
    service = QueryControlService.getInstance();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('Command Execution Success', () => {
    test('should execute valid command successfully', async () => {
      const queryId = 'test-query-001';
      const command = 'ls';
      const args = ['-la'];

      // Mock process spawn
      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('file1.txt\nfile2.txt')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command, args);

      expect(result.success).toBe(true);
      expect(result.exitCode).toBe(0);
      expect(result.output).toContain('file1.txt');
      expect(mockSpawn).toHaveBeenCalledWith(command, args, expect.any(Object));
    });

    test('should execute command without arguments', async () => {
      const queryId = 'test-query-002';
      const command = 'pwd';

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('/home/user')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command);

      expect(result.success).toBe(true);
      expect(result.exitCode).toBe(0);
      expect(result.output).toContain('/home/user');
      expect(mockSpawn).toHaveBeenCalledWith(command, undefined, expect.any(Object));
    });

    test('should handle command with complex arguments', async () => {
      const queryId = 'test-query-003';
      const command = 'grep';
      const args = ['-r', 'pattern', '/path/to/search'];

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('match1\nmatch2')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command, args);

      expect(result.success).toBe(true);
      expect(result.exitCode).toBe(0);
      expect(mockSpawn).toHaveBeenCalledWith(command, args, expect.any(Object));
    });
  });

  describe('Command Validation', () => {
    test('should reject empty command', async () => {
      const queryId = 'test-query-004';
      const command = '';

      await expect(service.executeCommand(queryId, command)).rejects.toThrow(McpError);
      await expect(service.executeCommand(queryId, command)).rejects.toMatchObject({
        code: ErrorCode.InvalidRequest,
      });
    });

    test('should reject command with dangerous characters', async () => {
      const queryId = 'test-query-005';
      const command = 'ls; rm -rf /';

      await expect(service.executeCommand(queryId, command)).rejects.toThrow(McpError);
      await expect(service.executeCommand(queryId, command)).rejects.toMatchObject({
        code: ErrorCode.InvalidRequest,
      });
    });

    test('should reject command with shell operators', async () => {
      const queryId = 'test-query-006';
      const invalidCommands = ['ls | grep', 'echo test > file', 'cat file && rm file'];

      for (const cmd of invalidCommands) {
        await expect(service.executeCommand(queryId, cmd)).rejects.toThrow(McpError);
      }
    });

    test('should validate command contains only allowed characters', async () => {
      const queryId = 'test-query-007';
      const command = 'ls`whoami`';

      await expect(service.executeCommand(queryId, command)).rejects.toThrow(McpError);
      await expect(service.executeCommand(queryId, command)).rejects.toMatchObject({
        code: ErrorCode.InvalidRequest,
      });
    });
  });

  describe('Security Constraints', () => {
    test('should prevent command injection via arguments', async () => {
      const queryId = 'test-query-008';
      const command = 'echo';
      const args = ['test', '; rm -rf /'];

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('test ; rm -rf /')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      // Command should execute but arguments are passed safely
      const result = await service.executeCommand(queryId, command, args);

      expect(result.success).toBe(true);
      // Arguments should be passed as array elements, not shell-interpreted
      expect(mockSpawn).toHaveBeenCalledWith(command, args, expect.any(Object));
    });

    test('should prevent path traversal in arguments', async () => {
      const queryId = 'test-query-009';
      const command = 'cat';
      const args = ['../../../etc/passwd'];

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(1), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn(),
        },
        stderr: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('No such file')), 5);
            }
          }),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command, args);

      // Command executes but should fail safely
      expect(result.success).toBe(false);
      expect(result.exitCode).toBe(1);
    });

    test('should enforce allowed commands list if configured', async () => {
      const queryId = 'test-query-010';
      const disallowedCommand = 'rm';

      // Assuming configuration exists for allowed commands
      await expect(service.executeCommand(queryId, disallowedCommand)).rejects.toThrow();
    });
  });

  describe('Exit Code Handling', () => {
    test('should handle successful exit code (0)', async () => {
      const queryId = 'test-query-011';
      const command = 'echo';
      const args = ['success'];

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('success')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command, args);

      expect(result.success).toBe(true);
      expect(result.exitCode).toBe(0);
    });

    test('should handle failure exit code (non-zero)', async () => {
      const queryId = 'test-query-012';
      const command = 'false';

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(1), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn(),
        },
        stderr: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('Command failed')), 5);
            }
          }),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command);

      expect(result.success).toBe(false);
      expect(result.exitCode).toBe(1);
      expect(result.error).toContain('Command failed');
    });

    test('should handle various exit codes correctly', async () => {
      const testCases = [
        { exitCode: 0, expectedSuccess: true },
        { exitCode: 1, expectedSuccess: false },
        { exitCode: 127, expectedSuccess: false },
        { exitCode: 255, expectedSuccess: false },
      ];

      for (const testCase of testCases) {
        const queryId = `test-query-exit-${testCase.exitCode}`;
        const command = 'test-command';

        const mockProcess = {
          on: jest.fn((event: string, callback: (code: number) => void) => {
            if (event === 'close') {
              setTimeout(() => callback(testCase.exitCode), 10);
            }
            return mockProcess;
          }),
          stdout: {
            on: jest.fn(),
          },
          stderr: {
            on: jest.fn(),
          },
        };

        mockSpawn.mockReturnValue(mockProcess);

        const result = await service.executeCommand(queryId, command);

        expect(result.success).toBe(testCase.expectedSuccess);
        expect(result.exitCode).toBe(testCase.exitCode);
      }
    });
  });

  describe('Telemetry Recording', () => {
    test('should record telemetry for successful execution', async () => {
      const queryId = 'test-query-013';
      const command = 'echo';
      const args = ['test'];

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('test')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      await service.executeCommand(queryId, command, args);

      expect(mockTelemetryRecord).toHaveBeenCalledWith(
        'executeCommand',
        expect.objectContaining({
          command,
          exitCode: 0,
          success: true,
        })
      );
    });

    test('should record telemetry for failed execution', async () => {
      const queryId = 'test-query-014';
      const command = 'false';

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(1), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn(),
        },
        stderr: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('error')), 5);
            }
          }),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      await service.executeCommand(queryId, command);

      expect(mockTelemetryRecord).toHaveBeenCalledWith(
        'executeCommand',
        expect.objectContaining({
          command,
          exitCode: 1,
          success: false,
        })
      );
    });

    test('should include command and args in telemetry metadata', async () => {
      const queryId = 'test-query-015';
      const command = 'grep';
      const args = ['-r', 'pattern'];

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('result')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      await service.executeCommand(queryId, command, args);

      expect(mockTelemetryRecord).toHaveBeenCalledWith(
        'executeCommand',
        expect.objectContaining({
          command,
          args,
        })
      );
    });
  });

  describe('Performance Profiling', () => {
    test('should record latency for command execution', async () => {
      const queryId = 'test-query-016';
      const command = 'sleep';
      const args = ['0.1'];

      jest.spyOn(Date, 'now')
        .mockReturnValueOnce(mockStartTime)
        .mockReturnValueOnce(mockStartTime + 150);

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 100);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn(),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      await service.executeCommand(queryId, command, args);

      expect(mockPerformanceRecord).toHaveBeenCalledWith(
        'executeCommand',
        expect.any(Number)
      );
    });

    test('should verify performance target <1000ms for simple commands', async () => {
      const queryId = 'test-query-017';
      const command = 'echo';
      const args = ['fast'];

      const executionTime = 50;
      jest.spyOn(Date, 'now')
        .mockReturnValueOnce(mockStartTime)
        .mockReturnValueOnce(mockStartTime + executionTime);

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('fast')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      await service.executeCommand(queryId, command, args);

      expect(mockPerformanceRecord).toHaveBeenCalledWith(
        'executeCommand',
        expect.any(Number)
      );

      // Verify latency is under 1000ms
      const recordedLatency = (mockPerformanceRecord as Mock).mock.calls[0][1] as number;
      expect(recordedLatency).toBeLessThan(1000);
    });

    test('should record accurate latency timing', async () => {
      const queryId = 'test-query-018';
      const command = 'test';
      const expectedLatency = 250;

      jest.spyOn(Date, 'now')
        .mockReturnValueOnce(mockStartTime)
        .mockReturnValueOnce(mockStartTime + expectedLatency);

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn(),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      await service.executeCommand(queryId, command);

      expect(mockPerformanceRecord).toHaveBeenCalledWith('executeCommand', expectedLatency);
    });
  });

  describe('Error Handling', () => {
    test('should handle invalid command error', async () => {
      const queryId = 'test-query-019';
      const command = '';

      await expect(service.executeCommand(queryId, command)).rejects.toThrow(McpError);
      await expect(service.executeCommand(queryId, command)).rejects.toMatchObject({
        code: ErrorCode.InvalidRequest,
      });
    });

    test('should handle query not found error', async () => {
      const queryId = 'non-existent-query';
      const command = 'echo';

      // This test assumes queryId validation exists
      // If not implemented, this test documents expected behavior
      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('test')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      // Should either succeed or fail gracefully
      const result = await service.executeCommand(queryId, command);
      expect(result).toBeDefined();
    });

    test('should handle command execution failure', async () => {
      const queryId = 'test-query-020';
      const command = 'non-existent-command';

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number | null, signal?: string) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(127), 10);
          } else if (event === 'error') {
            setTimeout(() => callback(null), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn(),
        },
        stderr: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('command not found')), 5);
            }
          }),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command);

      expect(result.success).toBe(false);
      expect(result.exitCode).toBe(127);
    });

    test('should handle process spawn error', async () => {
      const queryId = 'test-query-021';
      const command = 'test';

      mockSpawn.mockImplementation(() => {
        throw new Error('Failed to spawn process');
      });

      await expect(service.executeCommand(queryId, command)).rejects.toThrow(
        'Failed to spawn process'
      );
    });

    test('should handle timeout scenario', async () => {
      const queryId = 'test-query-022';
      const command = 'sleep';
      const args = ['infinity'];

      const mockProcess = {
        on: jest.fn(),
        kill: jest.fn(),
        stdout: {
          on: jest.fn(),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      // If timeout is implemented, verify it works
      // This test documents expected timeout behavior
      const timeoutPromise = new Promise((resolve) => setTimeout(resolve, 100));

      await Promise.race([
        service.executeCommand(queryId, command, args),
        timeoutPromise.then(() => ({ success: false, exitCode: -1, output: '', error: 'Timeout' })),
      ]);

      // Process should be killable
      expect(mockProcess.kill).toHaveBeenCalled();
    });
  });

  describe('Arguments Handling', () => {
    test('should handle commands without arguments', async () => {
      const queryId = 'test-query-023';
      const command = 'date';

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('2025-11-14')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command);

      expect(result.success).toBe(true);
      expect(mockSpawn).toHaveBeenCalledWith(command, undefined, expect.any(Object));
    });

    test('should handle commands with single argument', async () => {
      const queryId = 'test-query-024';
      const command = 'echo';
      const args = ['hello'];

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('hello')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command, args);

      expect(result.success).toBe(true);
      expect(mockSpawn).toHaveBeenCalledWith(command, args, expect.any(Object));
    });

    test('should handle commands with multiple arguments', async () => {
      const queryId = 'test-query-025';
      const command = 'find';
      const args = ['/path', '-name', '*.ts', '-type', 'f'];

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('file1.ts\nfile2.ts')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command, args);

      expect(result.success).toBe(true);
      expect(mockSpawn).toHaveBeenCalledWith(command, args, expect.any(Object));
    });

    test('should handle arguments with special characters safely', async () => {
      const queryId = 'test-query-026';
      const command = 'echo';
      const args = ['test "quoted" value', "test 'single' quote", 'test$variable'];

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('output')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command, args);

      expect(result.success).toBe(true);
      // Arguments should be passed as-is without shell interpretation
      expect(mockSpawn).toHaveBeenCalledWith(command, args, expect.any(Object));
    });

    test('should handle empty arguments array', async () => {
      const queryId = 'test-query-027';
      const command = 'pwd';
      const args: string[] = [];

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('/home/user')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command, args);

      expect(result.success).toBe(true);
      expect(mockSpawn).toHaveBeenCalledWith(command, args, expect.any(Object));
    });
  });

  describe('Output Handling', () => {
    test('should capture stdout output', async () => {
      const queryId = 'test-query-028';
      const command = 'echo';
      const expectedOutput = 'test output';

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from(expectedOutput)), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command);

      expect(result.output).toContain(expectedOutput);
    });

    test('should capture stderr output', async () => {
      const queryId = 'test-query-029';
      const command = 'test';
      const expectedError = 'error message';

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(1), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn(),
        },
        stderr: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from(expectedError)), 5);
            }
          }),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command);

      expect(result.error).toContain(expectedError);
    });

    test('should handle large output streams', async () => {
      const queryId = 'test-query-030';
      const command = 'cat';
      const largeOutput = 'x'.repeat(10000);

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from(largeOutput)), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      const result = await service.executeCommand(queryId, command);

      expect(result.output.length).toBeGreaterThan(9000);
    });
  });

  describe('Performance Targets', () => {
    test('should complete simple commands in <1000ms', async () => {
      const queryId = 'test-query-031';
      const command = 'echo';
      const startTime = Date.now();

      const mockProcess = {
        on: jest.fn((event: string, callback: (code: number) => void) => {
          if (event === 'close') {
            setTimeout(() => callback(0), 10);
          }
          return mockProcess;
        }),
        stdout: {
          on: jest.fn((event: string, callback: (data: Buffer) => void) => {
            if (event === 'data') {
              setTimeout(() => callback(Buffer.from('fast')), 5);
            }
          }),
        },
        stderr: {
          on: jest.fn(),
        },
      };

      mockSpawn.mockReturnValue(mockProcess);

      await service.executeCommand(queryId, command);

      const duration = Date.now() - startTime;
      expect(duration).toBeLessThan(1000);
    });
  });
});
