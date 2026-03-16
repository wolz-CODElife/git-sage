import type { ReactNode } from "react";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import styles from "./index.module.css";

function Hero(): ReactNode {
  return (
    <header className={styles.hero}>
      <div className={styles.heroInner}>
        <div className={styles.badge}>Local AI · No Cloud · Open Source</div>
        <h1 className={styles.heroTitle}>git-sage</h1>
        <p className={styles.heroSubtitle}>
          AI code review that runs on your machine.<br />
          Catches issues before they reach your repo.
        </p>
        <div className={styles.heroTerminal}>
          <div className={styles.terminalBar}>
            <span />
            <span />
            <span />
            <code className={styles.terminalTitle}>~/my-project</code>
          </div>
          <pre className={styles.terminalBody}>{`$ git push

  Staged: 1 file(s)  +6 / -0

  Issues  (1 found)

  ●  SECRET_KEY is hardcoded on line 14.

  ╭──────────────────────────────────╮
  │  ✗  REVISE                       │
  │  Push aborted by git-sage.       │
  ╰──────────────────────────────────╯`}</pre>
        </div>
        <div className={styles.heroCtas}>
          <Link className={styles.ctaPrimary} to="/docs/">
            Get started →
          </Link>
          <Link
            className={styles.ctaSecondary}
            to="https://github.com/wolz-CODElife/git-sage"
          >
            View on GitHub
          </Link>
        </div>
      </div>
    </header>
  );
}

const PrivacyIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 48 48">
    <path fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" d="M22.2 4.86L6.69 11.25V27C6.69 35.44 24 43.5 24 43.5S41.31 35.44 41.31 27V11.25L25.8 4.86a4.68 4.68 0 0 0-3.6 0"/>
    <rect width="17.39" height="13.4" x="15.31" y="19.26" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" rx="1.05"/>
    <path fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" d="M18.25 19.26v-2.41a5.75 5.75 0 0 1 11.5 0v2.41"/>
    <circle cx="24" cy="25.96" r="2.23" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const GitIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24">
    <g fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2">
      <path d="M4 18a2 2 0 1 0 4 0a2 2 0 1 0-4 0M4 6a2 2 0 1 0 4 0a2 2 0 1 0-4 0m12 12a2 2 0 1 0 4 0a2 2 0 1 0-4 0M6 8v8"/>
      <path d="M11 6h5a2 2 0 0 1 2 2v8"/>
      <path d="m14 9l-3-3l3-3"/>
    </g>
  </svg>
);

const AIIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
    <path fill="currentColor" d="M19 22v-2h1v-7h-1v-2h4v2h-1v7h1v2zm-3.5 0h2L14 11h-3L7.503 22h2l.601-2h4.778zm-4.794-4l1.628-5.411l.256-.003L14.264 18zM32 4h-4V0h-2v4h-4v2h4v4h2V6h4zm-2 8h2v2h-2zM18 0h2v2h-2z"/>
    <path fill="currentColor" d="M32 32H0V0h14v2H2v28h28V18h2z"/>
  </svg>
);

const ExtensibleIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 16 16">
    <path fill="currentColor" d="M3.5 1A2.5 2.5 0 0 0 1 3.5v7A2.5 2.5 0 0 0 3.5 13h1.992a2.5 2.5 0 0 1 .242-.28l.72-.72H3.5A1.5 1.5 0 0 1 2 10.5V5h10v.026a4.5 4.5 0 0 1 1 .004V3.5A2.5 2.5 0 0 0 10.5 1zm5.431 5.724l-.577-.578a.5.5 0 1 0-.708.708l.745.744q.216-.461.54-.874m-2.577.13a.5.5 0 1 0-.708-.708l-2 2a.5.5 0 0 0 0 .708l2 2a.5.5 0 0 0 .708-.708L4.707 8.5zm6.538-.83c.366.042.471.48.21.742l-.975.975a1.507 1.507 0 1 0 2.132 2.132l.975-.975c.261-.261.7-.156.742.21a3.518 3.518 0 0 1-4.676 3.723l-2.726 2.727a1.507 1.507 0 1 1-2.132-2.132L9.168 10.7a3.518 3.518 0 0 1 3.724-4.676"/>
  </svg>
);

const DepsIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24">
    <path fill="currentColor" d="M11.15 12.335v9.18a.6.6 0 0 1-.15-.08l-6.51-3.91a1.9 1.9 0 0 1-.7-.7a1.9 1.9 0 0 1-.25-1v-8.07zm9.31-4.58v8.1a2.1 2.1 0 0 1-.27.95a1.74 1.74 0 0 1-.69.71l-6.51 3.91l-.14.07v-9.17l3.26-2v2.77a.85.85 0 1 0 1.7 0v-3.74zm-5.18 1.15l-3.28 2l-7.66-4.6l.11-.07l3.06-1.63zm4.37-2.62l-2.71 1.62l-7.64-4.28l1.66-.87a2 2 0 0 1 1-.27a2.1 2.1 0 0 1 1 .28l6.47 3.46a.5.5 0 0 1 .22.06"/>
  </svg>
);

const OpenSourceIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24">
    <path fill="currentColor" d="M13 14c-3.36 0-4.46 1.35-4.82 2.24C9.25 16.7 10 17.76 10 19a3 3 0 0 1-3 3a3 3 0 0 1-3-3c0-1.31.83-2.42 2-2.83V7.83A2.99 2.99 0 0 1 4 5a3 3 0 0 1 3-3a3 3 0 0 1 3 3c0 1.31-.83 2.42-2 2.83v5.29c.88-.65 2.16-1.12 4-1.12c2.67 0 3.56-1.34 3.85-2.23A3.01 3.01 0 0 1 14 7a3 3 0 0 1 3-3a3 3 0 0 1 3 3c0 1.34-.88 2.5-2.09 2.86C17.65 11.29 16.68 14 13 14m-6 4a1 1 0 0 0-1 1a1 1 0 0 0 1 1a1 1 0 0 0 1-1a1 1 0 0 0-1-1M7 4a1 1 0 0 0-1 1a1 1 0 0 0 1 1a1 1 0 0 0 1-1a1 1 0 0 0-1-1m10 2a1 1 0 0 0-1 1a1 1 0 0 0 1 1a1 1 0 0 0 1-1a1 1 0 0 0-1-1"/>
  </svg>
);

function Features(): ReactNode {
  const items = [
    {
      icon: <PrivacyIcon />,
      title: "Fully private",
      desc: "Your code never leaves your machine. No API keys, no subscriptions, no data sent anywhere.",
    },
    {
      icon: <GitIcon />,
      title: "Git-native",
      desc: "Installs as a pre-push hook. Works automatically on every push; no new commands to remember.",
    },
    {
      icon: <AIIcon />,
      title: "Code-specialized AI",
      desc: "Uses qwen2.5-coder:7b: a model trained on code that understands diffs, spots real bugs, not style.",
    },
    {
      icon: <ExtensibleIcon />,
      title: "Extensible",
      desc: "Swap models, customize the prompt, add your own rules. One file to edit: prompt.py.",
    },
    {
      icon: <DepsIcon />,
      title: "Light dependencies",
      desc: "Just Python, Ollama, and three pip packages. Runs on any laptop without a GPU.",
    },
    {
      icon: <OpenSourceIcon />,
      title: "Open source",
      desc: "MIT licensed. Fork it, extend it, use it in your own tools.",
    },
  ];

  return (
    <section className={styles.features}>
      <div className={styles.featuresGrid}>
        {items.map((f) => (
          <div key={f.title} className={styles.featureCard}>
            <div className={styles.featureIcon}>{f.icon}</div>
            <h3 className={styles.featureTitle}>{f.title}</h3>
            <p className={styles.featureDesc}>{f.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function QuickStart(): ReactNode {
  return (
    <section className={styles.quickstart}>
      <h2 className={styles.sectionTitle}>Up and running in 4 commands</h2>
      <div className={styles.steps}>
        {[
          { n: "1", cmd: "brew install ollama && ollama pull qwen2.5-coder:7b", label: "Install Ollama + model" },
          { n: "2", cmd: "pip install git-sage", label: "Install git-sage" },
          { n: "3", cmd: "git-sage install", label: "Hook into your repo" },
          { n: "4", cmd: "git push", label: "Push as normal; review runs automatically" },
        ].map((s) => (
          <div key={s.n} className={styles.step}>
            <div className={styles.stepNumber}>{s.n}</div>
            <div className={styles.stepContent}>
              <code className={styles.stepCmd}>{s.cmd}</code>
              <span className={styles.stepLabel}>{s.label}</span>
            </div>
          </div>
        ))}
      </div>
      <Link className={styles.ctaPrimary} to="/docs/installation">
        Full installation guide →
      </Link>
    </section>
  );
}

export default function Home(): ReactNode {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout title={siteConfig.title} description={siteConfig.tagline}>
      <main>
        <Hero />
        <Features />
        <QuickStart />
      </main>
    </Layout>
  );
}