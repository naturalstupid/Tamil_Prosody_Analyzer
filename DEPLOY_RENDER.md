# Deploy YaappaRiSeyali to Render

## Recommended: Docker deployment

1. Push this folder to a GitHub, GitLab, or Bitbucket repository. Keep `Dockerfile`, `requirements-web.txt`, `render.yaml`, and `main.py` in the repository root.
2. In Render, choose **New > Web Service** and connect the repository.
3. Select the **Docker** runtime. Render should detect the root `Dockerfile`.
4. Use `/` as the health-check path.
5. Deploy. No custom start command is required because the Dockerfile runs `python main.py`.

`main.py` is already Render-compatible because it reads the `PORT` environment variable and binds to `0.0.0.0`:

```python
port = int(os.environ.get('PORT', 8080))
ui.run(host='0.0.0.0', port=port, reload=False)
```

## Non-Docker alternative

Create a Python Web Service with:

- Build command: `pip install -r requirements-web.txt`
- Start command: `python main.py`
- Python version: 3.11
- Health-check path: `/`

## Notes

- Use one Render instance unless you externalize NiceGUI state/session handling. The included configuration runs one Python process.
- Files written to the container filesystem are ephemeral on Render. The current web app downloads analysis to the user's browser, so no persistent disk is required for that feature.
- `setup.py` contains invalid standard-library entries (`itertools`, `operator`, `collections`, and `enum`) in `install_requires`. The deployment deliberately does not run `pip install .`; do not add it to the build command unless `setup.py` is corrected.
- If a future NiceGUI upgrade introduces an incompatibility, replace the version range in `requirements-web.txt` with the exact version from a successful deployment.
