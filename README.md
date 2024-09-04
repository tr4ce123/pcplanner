<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/tr4ce123/pcplanner">
    <img src="images/PCPlannerlogo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">PCPlanner</h3>

  <p align="center">
    A full-stack web application designed to make building your own PC as simple as possible.
    <br />
<!--     <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br /> -->
    <br />
    <a href="https://thepcplanner.com">View Live Site</a>
    ·
    <a href="#contact">Contact</a>
<!--     ·
    <a href="https://github.com/github_username/repo_name/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a> -->
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
<!--     <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li> -->
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#easy-builder-feature">Easy Builder</a></li>
        <li><a href="#builder-feature">Builder</a></li>
        <li><a href="#ai-insights-feature">AI Insights</a></li>
      </ul>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Landing Page][landing-page]](https://thepcplanner.com)

### Key Features

- **Smart Budgeting:** Enter your budget, and PCPlanner will recommend the best components that fit within your price range, ensuring you get the most value for your money.
- **Easy Builder Mode:** For beginners, the Easy Builder allows you to input your budget and get instant recommendations without the need to specify complex options.
- **Advanced Customization:** For those who want more control, the Builder mode lets you choose specifications such as chipset, usage, and network options to fine-tune your build.
- **AI-Powered Insights:** Ask ChatGPT for advice and insights on your build, including trade-offs and future-proofing tips, ensuring you make informed decisions.
- **Extensive Database:** PCPlanner uses an algorithm to search through over 3,000 components, making the process of finding the right parts quick and accurate.

### Project Goals

The primary goal of PCPlanner is to simplify the PC building experience by taking away the countless hours of searching required to find the best components for your budget. I wanted to create a website that is visually appealing and, more importantly, has fluid and easy user experience. PCPlanner should be an easy to use tool that gives quality reccomendations rather than being a marketing scheme. Many websites like the one I have created exist, but they simply reccomend a pre-set list of parts rather than dynamically sifting through a database of components.

This project aims to elimate the confusion for new, and even experienced users by offering a real list of compatible components by simply entering your budget.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

* [![Angular][Angular.io]][Angular-url]
* [![DjangoREST][DjangoREST]][Django-url]
* [![ChatGPT][ChatGPT]][ChatGPT-url]
* [![GithubPages][GithubPages]][GithubPages-url]
* [![Postgres][Postgres]][Postgres-url]
* ![Typescript]
* ![Python]
* ![HTML5]
* ![CSS]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED 
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```
-->




## Usage

### Easy Builder Feature

The purpose of this component is, well... to make an easy build. 

![easy-builder-page]

First, navigate to `thepcplanner.com/easybuilder` and make sure to read the notes at the top! They are important for understanding the time the components were added. Scroll down until you see the form to enter your budget.

![enter-budget]

Simply enter your budget as a plain integer and click the `Create My PC` button.

![custom-build]

After waiting a second or two, your custom build will appear. This component provides all of the information you need to build the PC and buy the parts. The `Buy Now` button links to the pcpartpicker link where you can see the full list of specs and pricing. 


### Builder Feature

The Builder feature is very similar, but it adds a layer of complexity. Users are allowed to include additional criteria for the computer they want generated.

First, navigate to `pcplanner.com/builder` and again, make sure to read the notes at the top! They really are important.

Now, scroll down to the preferences form at the bottom of the page. Once you complete a step on the form, you are allowed to go back and edit it however you'd like. 

#### Step 1
![form-1]

First, you want to set your budget to whatever you feel comfortable paying.

#### Step 2
![form-2]

Next, specify whether you want to use your PC for gaming, or productivity.

#### Step 3
![form-3]

Then, choose between Intel and AMD for your brand of CPU. Either one works here and you can research the difference between the two.

#### Step 4
![form-4]

For the fourth step, specify whether you need to connect to WiFi. Some motherboards are not equipped with the necessary parts to connect to the internet wirelessly.

#### Step 5
![form-5]
Finally, submit your form by pressing the button

#### Your Build
![custom-build2]
Your results should pop up in a few seconds or less and here is the PC that best matches the given preferences!

### AI Insights Feature

The AI Insights section acts as an agent to interact with ChatGPT's 4o model. Once you click the `Build Insights with AI` button, you will see a form pop up as shown below.

![insights]
![insights-form]

This form allows you to type any query you want to ask ChatGPT about your component selection and it even has some suggested questions. These questions have autocorrect that filters them as an option or not as the user is typing. When you're done with the form, submit it.

![insights-section]
You should see this text be generated with a typing animation and it will show you the response!

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] UI/UX
  - [x] Add appealing landing page
  - [x] Toolbar and footer
    - [ ] Make footer sticky: In progress
  - [ ] Animations: In progress
  - [ ] Page Layout: In progress
  - [ ] About Page: In progress
- [x] Builder / Easy Builder
  - [x] Create preferences form
  - [x] Implement backend recommendation algorithm
- [x] ChatGPT Integration
  - [x] Backend API integration
  - [x] AI insights section
  - [x] AI query form
  - [ ] Optimize backend query: In progress
- [x] Database
  - [x] Webscrape for parts
  - [x] Setup PostgreSQL backend
  - [x] Connect database to backend
- [ ] User Authentication: In progress / Questionable
- [x] Deployment
  - [x] Configure Railway deployment for database and backend
  - [x] Deploy on Github Pages for frontend

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Trace Glasby - [My Personal Website](https://traceglasby.com) - gglasby@unc.edu

Project Link: [https://github.com/tr4ce123/pcplanner](https://github.com/tr4ce123/pcplanner)

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/tr4ce123/pcplanner.svg?style=for-the-badge
[license-url]: https://github.com/tr4ce123/pcplanner/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/gglasby04
[landing-page]: images/LandingPage.png
[easy-builder-page]: images/EasyBuilderPage.png
[enter-budget]: images/EnterBudget.png
[custom-build]: images/CustomBuild.png
[custom-build2]: images/CustomBuild2.png
[form-1]: images/BuilderForm1.png
[form-2]: images/BuilderForm2.png
[form-3]: images/BuilderForm3.png
[form-4]: images/BuilderForm4.png
[form-5]: images/BuilderForm5.png
[insights]: images/Insights.png
[insights-form]: images/InsightsForm.png
[insights-section]: images/InsightsSection.png


<!-- Badge Links -->
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[DjangoREST]: https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray
[Django-url]: https://www.django-rest-framework.org/#development
[ChatGPT]: https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white
[ChatGPT-url]: https://platform.openai.com/docs/api-reference/introduction
[GithubPages]: https://img.shields.io/badge/github%20pages-121013?style=for-the-badge&logo=github&logoColor=white
[GithubPages-url]: https://pages.github.com/
[Postgres]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://www.postgresql.org/
[TypeScript]: https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[HTML5]: https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white
[CSS]: https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white
