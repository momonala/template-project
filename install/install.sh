set -e  # Exit immediately if a command exits with a non-zero status

# Colors for output
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "✅ Installing uv (Python package manager)"
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
else
    echo "✅ uv is already installed. Updating to latest version."
    uv self update
fi

echo "✅ Installing project dependencies with uv"
uv sync

# Extract configuration from pyproject.toml using config CLI
echo ""
echo -e "${GREEN}📋 Configuration:${NC}"
service_name=$(uv run config --project-name)
# Uncomment based on your project needs:
# service_port=$(uv run config --flask-port)
# tunnel_name=$(uv run config --tunnel-name)
# domain_suffix=$(uv run config --domain-suffix)

# Display all configuration in a nice table
echo "📋 Configuration:"
{
    uv run config --all | while IFS='=' read -r key value; do
        echo -e "   ${CYAN}${key}${NC}|${YELLOW}${value}${NC}"
    done
    # Add any computed values:
    # echo -e "   ${CYAN}cloudflare_domain${NC}|${YELLOW}${service_name}.${domain_suffix}${NC}"
} | column -t -s '|'
echo ""

echo "✅ Copying service file to systemd directory"
sudo cp install/projects_${service_name}.service /lib/systemd/system/projects_${service_name}.service
sudo cp install/projects_${service_name}data-backup-scheduler.service /lib/systemd/system/projects_${service_name}data-backup-scheduler.service

echo "✅ Setting permissions for the service file"
sudo chmod 644 /lib/systemd/system/projects_${service_name}.service
sudo chmod 644 /lib/systemd/system/projects_${service_name}data-backup-scheduler.service

echo "✅ Reloading systemd daemon"
sudo systemctl daemon-reload
sudo systemctl daemon-reexec

echo "✅ Enabling the service: projects_${service_name}.service"
sudo systemctl enable projects_${service_name}.service
sudo systemctl enable projects_${service_name}data-backup-scheduler.service
sudo systemctl restart projects_${service_name}.service
sudo systemctl restart projects_${service_name}data-backup-scheduler.service
sudo systemctl status projects_${service_name}.service --no-pager
sudo systemctl status projects_${service_name}data-backup-scheduler.service --no-pager

# Uncomment if you have Cloudflare tunnel configured:
# echo "✅ Adding Cloudflared service"
# service_port=$(uv run config --flask-port)
# tunnel_name=$(uv run config --tunnel-name)
# domain_suffix=$(uv run config --domain-suffix)
# /home/mnalavadi/add_cloudflared_service.sh ${service_name}.${domain_suffix} $service_port
# echo "✅ Configuring Cloudflared DNS route"
# cloudflared tunnel route dns ${tunnel_name} ${service_name}.${domain_suffix}
# echo "✅ Restarting Cloudflared service"
# sudo systemctl restart cloudflared

echo "✅ Setup completed successfully! 🎉"
