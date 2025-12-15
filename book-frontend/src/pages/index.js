import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/module-1/ros2-fundamentals">
            Read the Book 📚
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Practical AI & Robotics <head />">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--4">
                <h3>ROS 2 Fundamentals</h3>
                <p>Learn the basics of Robot Operating System 2 for humanoid robotics applications.</p>
              </div>
              <div className="col col--4">
                <h3>Digital Twin Development</h3>
                <p>Explore digital twin technology for simulating and testing humanoid robots.</p>
              </div>
              <div className="col col--4">
                <h3>Vision-Language-Action Models</h3>
                <p>Discover how VLA models enable humanoid robots to perceive and interact with the world.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}