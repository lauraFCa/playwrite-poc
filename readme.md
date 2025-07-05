# Selenium to Playwright Migration Project

[Run Selenium Tests](https://github.com/lauraFCa/playwrite-poc/actions/workflows/run_tests.yml)

## Overview

This project demonstrates the migration process from Selenium to Playwright for automated browser testing in C#/.NET.   
The repository contains a functional Selenium test suite that will be migrated to Playwright while maintaining the same test coverage and functionality.

## Project Structure

```
TestingStuff/
├── TestProject/
│   ├── Components/         # UI component abstractions
│   │   ├── BaseComponent.cs
│   │   ├── Button.cs
│   │   ├── Input.cs
│   │   ├── Label.cs
│   │   └── Navigation.cs
│   ├── Data/               # Test data models
│   │   └── PersonData.cs
│   ├── Pages/              # Page object models
│   │   ├── FormPage.cs
│   │   └── GithubPage.cs
│   ├── Tests/              # Test cases
│   │   ├── FormPageTests.cs
│   │   └── GithubHomeTests.cs
│   └── TestBase.cs         # Base test class with setup/teardown
├── run_tests.py            # Python script for test execution with retry logic
└── retry.runsettings       # Settings for test retry mechanism
```

## Current Implementation (Selenium)

The current implementation uses:

- **Selenium WebDriver** (v4.21.0)
- **MSTest** for the test framework
- **Page Object Model** design pattern
- **Component-based architecture** for UI elements
- **GitHub Actions** for CI/CD pipeline

## Migration Plan to Playwright

### Phase 1: Setup and Environment Configuration

- [ ] Add Microsoft.Playwright NuGet package
- [ ] Replace Selenium WebDriver and ChromeDriver packages
- [ ] Update BaseComponent.cs to use Playwright's IBrowser/IPage instead of Selenium's IWebDriver
- [ ] Configure Playwright browsers (Chromium, Firefox, WebKit)

### Phase 2: Core Components Migration

- [ ] Update component classes (Button, Input, etc.) to use Playwright locators and methods
- [ ] Migrate from Selenium's By selectors to Playwright's locator patterns
- [ ] Update interaction methods (Click, TypeIn) to use Playwright's API

### Phase 3: Page Objects and Test Cases

- [ ] Update page objects to use Playwright's API
- [ ] Refactor test initialization and cleanup
- [ ] Adapt configuration handling for Playwright

### Phase 4: CI/CD and Reporting

- [ ] Update GitHub Actions workflow for Playwright
- [ ] Configure Playwright test reporting
- [ ] Adapt retry mechanism for Playwright tests

## Key Differences Between Selenium and Playwright

| Feature              | Selenium                         | Playwright                                    |
| -------------------- | -------------------------------- | --------------------------------------------- |
| Browser Support      | Chrome, Firefox, Edge, Safari    | Chromium, Firefox, WebKit                     |
| Auto-waiting         | Limited, requires explicit waits | Built-in auto-waiting for elements            |
| Network Interception | Limited capabilities             | Advanced request/response mocking             |
| Isolation            | Shared browser context           | Isolated browser contexts                     |
| Screenshots          | Basic capabilities               | Full-page, element-specific screenshots       |
| Mobile Emulation     | Limited                          | Comprehensive device emulation                |
| Selector Engines     | XPath, CSS                       | XPath, CSS, Text, TestID, plus custom engines |
| Video Recording      | Requires third-party tools       | Built-in capabilities                         |

## Getting Started

### Prerequisites

- .NET 8.0 SDK
- Visual Studio 2022 or VS Code
- Python 3.11+ (for test execution script)

### Running Tests (Current Selenium Implementation)

```powershell
# Run all tests
dotnet test

# Run specific test
dotnet test --filter "Name~Validate_Github_HomePage"

# Run tests with retry mechanism
python run_tests.py
```

### Running Tests (After Playwright Migration)

```powershell
# Install Playwright browsers
pwsh bin/Debug/net8.0/playwright.ps1 install

# Run all tests
dotnet test

# Run specific test
dotnet test --filter "Name~Validate_Github_HomePage"

# Run tests with retry mechanism
python run_tests.py
```

## Contributing

1. Create a feature branch (`git checkout -b feature/playwright-migration`)
2. Commit your changes (`git commit -m 'Migrate Button component to Playwright'`)
3. Push to the branch (`git push origin feature/playwright-migration`)
4. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

