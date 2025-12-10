# Docker Execution Environments

Secure, minimal Docker images for executing code in AI CodeForge.

## Available Images

### Python (python.Dockerfile)
- **Base**: python:3.11-slim
- **Packages**: pytest, requests, numpy, pandas, flask, fastapi, pydantic
- **User**: Non-root (runner:runner)
- **Size**: ~200MB

### JavaScript (javascript.Dockerfile)
- **Base**: node:18-slim
- **Packages**: jest, mocha, express, axios, lodash
- **User**: Non-root (runner:runner)
- **Size**: ~180MB

### TypeScript (typescript.Dockerfile)
- **Base**: node:18-slim
- **Packages**: typescript, ts-node, jest, @types packages
- **User**: Non-root (runner:runner)
- **Size**: ~190MB

## Building Images

```bash
# Build all images
docker build -t ai-codeforge-python:latest -f docker/python.Dockerfile .
docker build -t ai-codeforge-javascript:latest -f docker/javascript.Dockerfile .
docker build -t ai-codeforge-typescript:latest -f docker/typescript.Dockerfile .

# Or build specific image
docker build -t ai-codeforge-python:latest -f docker/python.Dockerfile .
```

## Security Features

All images include:
- ✅ Non-root user execution
- ✅ Minimal base images
- ✅ No unnecessary packages
- ✅ Read-only filesystem (enforced at runtime)
- ✅ Network disabled by default (enforced at runtime)
- ✅ Memory limits (enforced at runtime)
- ✅ CPU limits (enforced at runtime)
- ✅ No privileged access

## Runtime Security

When executed via DockerCodeExecutor, additional restrictions apply:
- `--read-only`: Read-only root filesystem
- `--network=none`: Network isolation
- `--memory=512m`: Memory limit
- `--cpu-quota=50000`: CPU limit (50% of one core)
- `--security-opt=no-new-privileges`: No privilege escalation
- `--cap-drop=ALL`: Drop all Linux capabilities
- `--tmpfs /tmp`: Writable /tmp with noexec,nosuid

## Usage

### Via DockerCodeExecutor

```python
from execution.docker_executor import DockerCodeExecutor

executor = DockerCodeExecutor()

# Execute Python code
result = executor.execute(
    code="print('Hello from Docker!')",
    language='python',
    timeout=30
)

print(result.output)  # "Hello from Docker!"
```

### Direct Docker Execution

```bash
# Run Python code
docker run --rm \
  --read-only \
  --network=none \
  --memory=512m \
  -v /path/to/code:/code:ro \
  ai-codeforge-python:latest \
  python /code/script.py

# Run JavaScript code
docker run --rm \
  --read-only \
  --network=none \
  --memory=512m \
  -v /path/to/code:/code:ro \
  ai-codeforge-javascript:latest \
  node /code/script.js
```

## Customization

To add more packages, edit the Dockerfile and rebuild:

```dockerfile
# Add to python.Dockerfile
RUN pip install --no-cache-dir \
    your-package-name>=1.0.0
```

Then rebuild:
```bash
docker build -t ai-codeforge-python:custom -f docker/python.Dockerfile .
```

## Pre-pulling Images

For faster execution, pre-pull images:

```python
executor = DockerCodeExecutor()
results = executor.pull_images()  # Pull all supported languages

# Or specific languages
results = executor.pull_images(['python', 'javascript'])
```

## Troubleshooting

### Docker Not Available
```
Error: Docker is not available. Install Docker to use sandboxed execution.
```
**Solution**: Install Docker Desktop or Docker Engine

### Permission Denied
```
Error: permission denied while trying to connect to the Docker daemon socket
```
**Solution**: Add your user to the docker group:
```bash
sudo usermod -aG docker $USER
# Then log out and back in
```

### Image Pull Timeout
```
Error: timeout pulling image
```
**Solution**: Check internet connection and Docker Hub status

### Container Out of Memory
```
Error: container killed (OOMKilled)
```
**Solution**: Increase memory limit:
```python
result = executor.execute(code, memory_limit="1g")
```

## Performance Tips

1. **Pre-pull images** before first use
2. **Use slim base images** (already done)
3. **Limit installed packages** to essentials
4. **Set appropriate timeouts** for your use case
5. **Monitor resource usage** and adjust limits

## Security Best Practices

1. ✅ Always use `--read-only` filesystem
2. ✅ Disable network unless required
3. ✅ Set memory and CPU limits
4. ✅ Run as non-root user
5. ✅ Drop all capabilities
6. ✅ Use `--security-opt=no-new-privileges`
7. ✅ Regular image updates
8. ✅ Scan images for vulnerabilities

## Updates

Keep images updated:
```bash
# Pull latest base images
docker pull python:3.11-slim
docker pull node:18-slim

# Rebuild
docker build --no-cache -t ai-codeforge-python:latest -f docker/python.Dockerfile .
```

## License

MIT License - See main project LICENSE file
