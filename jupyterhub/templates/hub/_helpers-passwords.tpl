{{- /*
    This file contains logic to lookup already
    generated passwords or generate a new.

    proxy.secretToken       / hub.config.JupyterHub.proxy_auth_token
    hub.cookieSecret        / hub.config.JupyterHub.cookie_secret
    auth.state.cryptoKey    / hub.config.CryptKeeper.keys

    Note that lookup logic returns falsy value when run with
    `helm diff upgrade`, so it is a bit troublesome to test.
*/}}

{{/*
    Returns given number of random Hex characters.

    - randNumeric 4 | atoi generates a random number in [0, 10^4)
      This is a range range evenly divisble by 16, but even if off by one,
      that last partial interval offsetting randomness is only 1 part in 625.
    - mod N 16 maps to the range 0-15
    - printf "%x" represents a single number 0-15 as a single hex character
*/}}
{{- define "jupyterhub.randHex" -}}
    {{- $result := "" }}
    {{- range $i := until . }}
        {{- $rand_hex_char := mod (randNumeric 4 | atoi) 16 | printf "%x" }}
        {{- $result = print $result $rand_hex_char }}
    {{- end }}
    {{- $result }}
{{- end }}

{{- define "jupyterhub.config.JupyterHub.proxy_auth_token" -}}
    {{- if .Values.proxy.secretToken }}
        {{- .Values.proxy.secretToken }}
    {{- else }}
        {{- $k8s_state := lookup "v1" "Secret" .Release.Namespace (include "jupyterhub.hub.fullname" .) | default (dict "data" (dict)) }}
        {{- if hasKey $k8s_state.data "JupyterHub.proxy_auth_token" }}
            {{- index $k8s_state.data "JupyterHub.proxy_auth_token" | b64dec }}
        {{- else }}
            {{- randAlphaNum 64 }}
        {{- end }}
    {{- end }}
{{- end }}

{{- define "jupyterhub.config.JupyterHub.cookie_secret" -}}
    {{- if .Values.hub.cookieSecret }}
        {{- .Values.hub.cookieSecret }}
    {{- else }}
        {{- $k8s_state := lookup "v1" "Secret" .Release.Namespace (include "jupyterhub.hub.fullname" .) | default (dict "data" (dict)) }}
        {{- if hasKey $k8s_state.data "JupyterHub.cookie_secret" }}
            {{- index $k8s_state.data "JupyterHub.cookie_secret" | b64dec }}
        {{- else }}
            {{- include "jupyterhub.randHex" 64 }}
        {{- end }}
    {{- end }}
{{- end }}

{{- define "jupyterhub.config.CryptKeeper.keys" -}}
    {{- if .Values.hub.config.CryptKeeper }}
        {{- .Values.hub.config.CryptKeeper.keys | join ";" }}
    {{- else }}
        {{- $k8s_state := lookup "v1" "Secret" .Release.Namespace (include "jupyterhub.hub.fullname" .) | default (dict "data" (dict)) }}
        {{- if hasKey $k8s_state.data "CryptKeeper.keys" }}
            {{- index $k8s_state.data "CryptKeeper.keys" | b64dec }}
        {{- else }}
            {{- include "jupyterhub.randHex" 64 }}
        {{- end }}
    {{- end }}
{{- end }}
