# Deploying Docusaurus to GitHub Pages

This guide explains how to deploy your Docusaurus site to GitHub Pages.

## Prerequisites

1.  A GitHub account.
2.  A GitHub repository containing your Docusaurus project (e.g., `your-username/your-docusaurus-repo`).
3.  `git` installed locally.
4.  `npm` or `yarn` installed locally (to run the Docusaurus build command).

## Steps

### 1. Configure `docusaurus.config.js`

Before deploying, you need to update your `docusaurus.config.js` file with the correct `url` and `baseUrl`.

*   `url`: This should be your GitHub Pages URL, typically `https://<your-username>.github.io`.
*   `baseUrl`: This is usually `/` unless your site is intended to be hosted in a subdirectory.

For example, if your GitHub username is `myroboticsbook`:
```javascript
// docusaurus.config.js
const config = {
  // ... other config
  url: 'https://myroboticsbook.github.io',
  baseUrl: '/',
  // ... other config
};
```
If you are using a custom domain, you can set the `url` to your custom domain (e.g., `https://myroboticsbook.com`).

### 2. Set up GitHub Pages in your Repository Settings

1.  Go to your GitHub repository page.
2.  Click on the **Settings** tab.
3.  In the left sidebar, click **Pages**.
4.  Under **Source**, select **Deploy from a branch**.
5.  Select the `gh-pages` branch and `/ (root)` as the folder. Click **Save**.
    *   Docusaurus will automatically create and push to the `gh-pages` branch during deployment.

### 3. Deploy using the Docusaurus Command

1.  Open a terminal in your Docusaurus project directory (where `docusaurus.config.js` is located).
2.  Ensure you are on the branch you want to deploy from (often `main` or `master`).
3.  Run the following command:
    ```bash
    npm run deploy
    ```
    or if you are using Yarn:
    ```bash
    yarn deploy
    ```
    This command will:
    *   Run `npm run build` (or `yarn build`) to create the static HTML files in the `build` folder.
    *   Push the contents of the `build` folder to the `gh-pages` branch of your repository.

### 4. View Your Deployed Site

GitHub Pages will automatically serve your site. It might take a few minutes for the first deployment to be live.
You can access your site at `https://<your-username>.github.io/<repository-name>/` (or `https://<your-username>.github.io/` if the repository name matches your username, or at your custom domain if configured).

### 5. Subsequent Deployments

For future updates, simply make your changes to your Docusaurus source files, commit them to your main branch, and run `npm run deploy` (or `yarn deploy`) again. This will update the `gh-pages` branch and your live site.

## Troubleshooting

*   **Site not loading correctly (e.g., blank page, missing styles):** Double-check your `url` and `baseUrl` in `docusaurus.config.js`. Ensure they match your GitHub Pages URL structure.
*   **"Command not found" errors:** Ensure `npm` or `yarn` is installed and accessible from your terminal.
*   **Permission errors pushing to `gh-pages`:** Ensure you have write permissions to the repository.