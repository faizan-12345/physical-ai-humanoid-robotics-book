import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import {translate} from '@docusaurus/Translate';
import Layout from '@theme/Layout';

export default function NotFound() {
  return (
    <Layout title={translate({id: 'theme.NotFound.title', message: 'Page Not Found'})}>
      <main className="container margin-vert--xl">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <h1 className="hero__title">{translate({id: 'theme.NotFound.title', message: 'Page Not Found'})}</h1>
            <p>{translate({id: 'theme.NotFound.p1', message: 'We could not find what you were looking for.'})}</p>
            <p>
              <Link to="/" className="button button--primary button--lg">
                {translate({id: 'theme.NotFound.link', message: 'Back to Homepage'})}
              </Link>
            </p>
          </div>
        </div>
      </main>
    </Layout>
  );
}