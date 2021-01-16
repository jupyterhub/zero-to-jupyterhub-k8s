{{- /*
    This file contains logic to lookup already
    generated passwords or generate a new.

    proxy.secretToken       / hub.config.JupyterHub.proxy_auth_token
    hub.cookieSecret        / hub.config.JupyterHub.cookie_secret
    auth.state.cryptoKey    / hub.config.CryptKeeper.keys
*/}}
{{- define "jupyterhub.config.JupyterHub.proxy_auth_token" -}}
    {{- if .Values.proxy.secretToken }}
        {{- .Values.proxy.secretToken }}
    {{- else }}
        {{- $k8s_state := lookup "v1" "Secret" .Release.Namespace "hub-secret" }}
        {{- if $k8s_state }}
            {{- with index $k8s_state "JupyterHub.proxy_auth_token" }}
                {{- . }}
            {{- end }}
        {{- else }}
            {{- randNumeric 32 }}
        {{- end }}
    {{- end }}
{{- end }}

{{- define "jupyterhub.config.JupyterHub.cookie_secret" -}}
    {{- if .Values.hub.cookieSecret }}
        {{- .Values.hub.cookieSecret }}
    {{- else }}
        {{- $k8s_state := lookup "v1" "Secret" .Release.Namespace "hub-secret" }}
        {{- if $k8s_state }}
            {{- with index $k8s_state "JupyterHub.cookie_secret" }}
                {{- . }}
            {{- end }}
        {{- else }}
            {{- randNumeric 32 }}
        {{- end }}
    {{- end }}
{{- end }}

{{- define "jupyterhub.config.CryptKeeper.keys" -}}
    {{- if .Values.hub.config.CryptKeeper }}
        {{- .Values.hub.config.CryptKeeper.keys | join ";" }}
    {{- else }}
        {{- $k8s_state := lookup "v1" "Secret" .Release.Namespace "hub-secret" }}
        {{- if $k8s_state }}
            {{- with index $k8s_state "CryptKeeper.keys" }}
                {{- . }}
            {{- end }}
        {{- else }}
            {{- randNumeric 32 }}
        {{- end }}
    {{- end }}
{{- end }}
