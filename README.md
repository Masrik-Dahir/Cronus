# Cronus: An Automated Feedback Tool for Concept Maps Comparing
[![Python Package using Conda](https://github.com/Masrik-Dahir/Cronus/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/Masrik-Dahir/Cronus/actions/workflows/python-package-conda.yml) [![CodeQL](https://github.com/Masrik-Dahir/Cronus/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Masrik-Dahir/Cronus/actions/workflows/codeql-analysis.yml)

Security And Forensics Engineering Lab, Virginia Commonwealth University

Faculty Professor: Dr. Irfan Ahmed

The repository is a research project which I have been conducting under the SAFE Lab of VCU. The project intends to compare camp files and provide similarities. It is written in python- the program also involves natural language processing and machine learning.

# Configuration
1. Install Graphviz
2. Clone the repository
3. Go to the repository folder
4. Run requirement.bat
# Run
```
python diagram.py <instructor_cxl_direcotry> <student_cxl_direcotry>
```
# Example (Ubuntu, Windows)
```
git clone "https://github.com/Masrik-Dahir/Cronus.git";
cd Cronus;
.\requirement.bat;
python diagram.py 'ConceptMapFiles\CXLFiles\ComputerSecurity\Instructor\Module1IntroductionComputerSecurity\Lesson1ComputerSecurityOverview\CS_Overview.cmap.cxl' 'ConceptMapFiles\CXLFiles\ComputerSecurity\Student\Module1IntroductionComputerSecurity\ICSAnonymous6.cmap.cxl';
```

# Result
![image](https://user-images.githubusercontent.com/69909265/179337465-116b2a65-2a7d-4816-bc2e-184237474f1c.png)

![image](https://user-images.githubusercontent.com/69909265/179337485-6140ceb8-6dbc-4c14-839a-b2e23295b091.png)
