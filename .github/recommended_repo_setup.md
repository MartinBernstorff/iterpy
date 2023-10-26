## Recommened setup for the repository
 ### Github Repository Settings
 These are all GitHub settings we recommend enabling, e.g. go to the repository's `Settings > General > Allow auto-merge`.

 * General
   * Pull Requests
     * Always suggest updating pull request branches 
     * Allow auto-merge
     * Automatically delete head branches

 * Branches
   * Add a branch protection rule for "main"
     * Require a pull request before merging
     * Require status checks to pass before merging
       * Require branches to be up to date before merging
       * Status checks that are required
     * Require conversation resolution before merging