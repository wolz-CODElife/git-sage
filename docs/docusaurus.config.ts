import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

const config: Config = {
  title: "git-sage",
  tagline: "Local AI code reviewer for your git workflow. Powered by Ollama",
  favicon: "img/favicon.ico",

  url: "https://wolz-codelife.github.io",
  baseUrl: "/git-sage/",

  organizationName: "wolz-CODElife",
  projectName: "git-sage",
  trailingSlash: false,

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: "./sidebars.ts",
          editUrl: "https://github.com/wolz-CODElife/git-sage/tree/master/docs/",
          routeBasePath: "docs",
        },
        blog: false,
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      defaultMode: "dark",
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: "git-sage",
      items: [
        {
          type: "docSidebar",
          sidebarId: "tutorialSidebar",
          position: "left",
          label: "Docs",
        },
        {
          href: "https://github.com/wolz-CODElife/git-sage",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Docs",
          items: [
            { label: "Getting Started", to: "/docs/" },
            { label: "Architecture", to: "/docs/architecture" },
            { label: "Contributing", to: "/docs/contributing" },
          ],
        },
        {
          title: "Community",
          items: [
            { label: "GitHub", href: "https://github.com/wolz-CODElife/git-sage" },
            { label: "Issues", href: "https://github.com/wolz-CODElife/git-sage/issues" },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} git-sage. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.oneDark,
      darkTheme: prismThemes.oneDark,
      additionalLanguages: ["bash", "python", "toml", "diff"],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;