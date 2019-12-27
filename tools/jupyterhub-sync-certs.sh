#!/usr/bin/env bash
###
## Execs into the hub container and generates internal certificates
## Afterwards it creates secrets from those internal certificates
###
set -euo pipefail

main() {
  cert_storage=$(mktemp -dt internal-ssl)
  output_dir="$cert_storage/internal-ssl"
  generate_certs
  create_secret "$output_dir/certipy.json"
}

generate_certs() {
  local pod tar_filename output_file
  tar_filename="internal-ssl.tgz"
  output_file="$cert_storage/$tar_filename"

  pod=$(kubectl get pod -l "app=jupyterhub,component=hub" --no-headers -o custom-columns=:metadata.name | head -n 1)
  kubectl exec "$pod" -- bash -c "rm -rf internal-ssl; jupyterhub -f /etc/jupyterhub/jupyterhub_config.py --generate-certs; tar -czf /tmp/$tar_filename internal-ssl/"
  kubectl cp "$pod:/tmp/$tar_filename" "$output_file"
  tar -xzf "$output_file" -C "$cert_storage/"
  ls -lah "$output_dir/"
}

create_secret() {
  local internal_ssl_dir dir_base output_dir path_to_certipy_json path_args

  path_to_certipy_json="${1?Expected path to generated certipy.json}"
  internal_ssl_dir="$(dirname "$path_to_certipy_json")"
  dir_base="${internal_ssl_dir%%/internal-ssl}"
  output_dir="$dir_base/generated_secrets"
  mkdir -p "$output_dir"
  path_args=()

  mapfile -t files < <(jq -r 'to_entries[] | .value.files | values[] | select(length > 0)' "$path_to_certipy_json" | sort -u)
  path_args+=("--from-file=$internal_ssl_dir/") # add ca_trusts
  for file in "${files[@]}"; do
    echo "Adding file $file"
    path_args+=("--from-file=$dir_base/$file")
  done

  echo "Generating secret"
  local secret_name="jupyterhub-certs"
  local secret_path="${output_dir}/${secret_name}.yaml"
  # shellcheck disable=SC2086 #intentional to add path_args
  kubectl create secret generic "${secret_name}" ${path_args[*]} --dry-run -o yaml > "$secret_path"
  kubectl apply -f "$secret_path"
}

main "$@"
