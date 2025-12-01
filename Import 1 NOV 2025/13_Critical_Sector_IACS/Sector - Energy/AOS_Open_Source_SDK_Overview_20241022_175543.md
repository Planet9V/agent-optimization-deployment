---
tags:
  intellihub_specific:
    - services
  technical_components:
    - e355_meter
    - intelligenx
---

# AOS Open-Source SDK Overview

Last updated: October 21, 2024, 23:45

## Introduction

The Advanced Operating System (AOS) Open-Source Software Development Kit (SDK) is a critical component of the IntelligenX smart meter system. Developed by Aetheros, this SDK provides developers with the tools and resources necessary to create, modify, and extend applications for the IntelligenX devices.

## GitHub Repository

The AOS SDK and related resources are hosted on GitHub under the Aetheros organization: https://github.com/Aetheros

## Key Components

1. **sdk-python**: Python SDK for AOS development
2. **device-sdk**: C++ SDK for device-level development
3. **sdk-dotnet**: .NET SDK for AOS development
4. **sdk-java**: Java SDK for AOS development
5. **aos-metering-app**: Sample application demonstrating the use of metering services
6. **aos-floating-neutral-app**: Example application for floating neutral detection
7. **aos-waveform-app**: Example application utilizing the E355 waveform provider service
8. **aos-openfmb-adapter**: OpenFMB adapter for AOS

## Language Support

The AOS SDK supports multiple programming languages, providing flexibility for developers:
- C++
- Python
- C#
- Java

## Key Features

1. **Multi-platform Support**: SDKs available for various development environments
2. **Sample Applications**: Practical examples demonstrating SDK usage and capabilities
3. **Device-specific Features**: Support for E355 meter-specific functionalities
4. **Open Standards**: Integration with open standards like OpenFMB
5. **Regular Updates**: Active maintenance and updates to the SDK repositories

## Security Considerations

1. **Open-Source Nature**: While providing transparency and community involvement, it also exposes potential vulnerabilities to a wider audience
2. **Dependency Management**: Careful management of third-party dependencies is crucial
3. **Version Control**: Proper version control and update processes are essential to maintain security
4. **Code Review**: Regular code reviews and security audits are necessary
5. **Community Contributions**: While valuable, community contributions must be carefully vetted

## Implications for IntelligenX System

1. **Customization**: Allows for tailored applications and features for specific deployment scenarios
2. **Third-party Integration**: Facilitates integration with various third-party systems and services
3. **Rapid Development**: Enables faster development and deployment of new features
4. **Security Challenges**: Requires ongoing vigilance and proactive security measures
5. **Community Engagement**: Potential for community-driven improvements and issue resolution

## Conclusion

The AOS Open-Source SDK is a powerful tool that enhances the flexibility and extensibility of the IntelligenX smart meter system. However, its open-source nature also introduces specific security considerations that must be carefully managed. Proper use of the SDK, combined with rigorous security practices, is essential for maintaining the integrity and security of the IntelligenX ecosystem.
