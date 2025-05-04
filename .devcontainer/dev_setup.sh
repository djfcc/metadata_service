curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'eval "$(uv generate-shell-completion bash)"' >> /home/devuser/.bashrc
echo "alias ll='ls -la'" >> /home/devuser/.bashrc