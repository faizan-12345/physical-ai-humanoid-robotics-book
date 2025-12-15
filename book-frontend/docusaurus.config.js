// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

import {themes as prismThemes} from 'prism-react-renderer';

// Determine the correct URL and base URL based on environment
const isDeployedToGitHubPages = process.env.NETLIFY === undefined && process.env.VERCEL === undefined;
const isDeployedToVercel = process.env.VERCEL === '1';

const siteUrl = isDeployedToVercel
  ? 'https://physical-ai-humanoid-robotics-book-nu.vercel.app'
  : 'https://faizan-12345.github.io';

const baseUrl = isDeployedToVercel
  ? '/'
  : '/physical-ai-humanoid-robotics-book/';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Humanoid Robotics Book',
  tagline: 'Practical AI & Robotics',
  favicon: 'img/favicon.ico',
  url: siteUrl,
  baseUrl: baseUrl,
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          showLastUpdateAuthor: true,
          showLastUpdateTime: true,
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],
  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Humanoid Robotics Book',
        logo: {
          alt: 'My Site Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Book',
          },
          {
            to: '/',
            label: 'Home',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [],
        copyright: `Copyright © ${new Date().getFullYear()} Humanoid Robotics Book. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
