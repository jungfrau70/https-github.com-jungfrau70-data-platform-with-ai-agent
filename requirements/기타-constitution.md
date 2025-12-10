# Speckit Constitution

This document outlines the core principles and standards for the Speckit project. These guidelines govern our approach to code quality, testing, user experience, and performance.

## 1. Code Quality

*   **Clarity Over Cleverness**: Code should be easy to read and understand. Favor explicit implementation over implicit magic. simpler is better.
*   **Consistency**: Adhere strictly to the project's linting and formatting rules. The codebase should look like it was written by a single person.
*   **Modularity**: Build small, reusable, and single-purpose functions and components.
*   **Documentation**: Document *why* complex logic exists, not just *what* it does. Keep comments up-to-date with code changes.
*   **Review**: All code changes must be reviewed. Constructive feedback is encouraged to maintain high standards.

## 2. Testing Standards

*   **Test-Driven Mindset**: Consider how code will be tested before writing it.
*   **Coverage**: Reference critical business logic must have unit tests. Integration tests should cover major user flows.
*   **Reliability**: Tests should be deterministic. Flaky tests are treated as broken and must be fixed immediately.
*   **Pyramid**: Maintain a healthy testing pyramid—many unit tests, fewer integration tests, and selective end-to-end tests.

## 3. User Experience Consistency

*   **Design System Compliance**: All UI components must utilize the established design tokens and components to ensure visual consistency.
*   **Responsiveness**: The application must function flawlessly across supported device sizes (Desktop, Tablet, Mobile).
*   **Accessibility (A11y)**: Building for accessibility is not optional. Semantic HTML and ARIA attributes should be used correctly to support assistive technologies.
*   **Feedback**: The interface must always provide feedback for user actions (e.g., loading states, success messages, error handling). Never leave the user guessing.

## 4. Performance Requirements

*   **Speed**: Prioritize fast load times and interactive responsiveness. Monitor Core Web Vitals (LCP, FID, CLS).
*   **Optimization**: Optimize assets (images, fonts, bundles) to minimize bandwidth and parsing time.
*   **Efficiency**: Avoid unnecessary re-renders in frontend components. Use efficient algorithms and data structures on the backend.
*   **Scalability**: Design systems that can handle growth in data and user traffic without degradation in performance.
