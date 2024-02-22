# tamemoji

A simple emoji drawing game.

### Development

Install all necessary dependencies:

```commandline
npm clean-install
```

Run the development server:

```commandline
npm run dev
```

Before committing, run the formatter and linter:

```commandline
npm run format
npm run lint
```

### Deployment
Copy `dist.env` to `.env` and fill in the necessary environment variables.

By default, frontend will consider `http://localhost:8000` as the backend server. 

You can change this by setting `VITE_BACKEND_URL` in `.env`.
