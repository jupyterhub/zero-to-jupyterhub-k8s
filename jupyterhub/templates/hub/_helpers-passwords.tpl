{{- /*
    This file contains logic to lookup already
    generated passwords or generate a new.

    proxy.secretToken       / hub.config.JupyterHub.proxy_auth_token
    hub.cookieSecret        / hub.config.JupyterHub.cookie_secret
    auth.state.cryptoKey    / hub.config.CryptKeeper.keys
*/}}

{{/*
    Returns given number of random Hex characters.

    In practice, it generates up to 100 randAlphaNum strings
    that are filtered from non-hex characters and augmented
    to the resulting string that is finally trimmed down.
*/}}
{{- define "jupyterhub.randHex" -}}
    {{- $result := "" }}
    {{- range $i := until 100 }}
        {{- if lt (len $result) . }}
            {{- $rand_list := randAlphaNum . | splitList "" -}}
            {{- $reduced_list := without $rand_list "g" "h" "i" "j" "k" "l" "m" "n" "o" "p" "q" "r" "s" "t" "u" "v" "w" "x" "y" "z" "A" "B" "C" "D" "E" "F" "G" "H" "I" "J" "K" "L" "M" "N" "O" "P" "Q" "R" "S" "T" "U" "V" "W" "X" "Y" "Z" }}
            {{- $rand_string := join "" $reduced_list }}
            {{- $result = print $result $rand_string -}}
        {{- end }}
    {{- end }}
    {{- $result | trunc . }}
{{- end }}

{{- define "jupyterhub.config.JupyterHub.proxy_auth_token" -}}
    {{- if .Values.proxy.secretToken }}
        {{- .Values.proxy.secretToken }}
    {{- else }}
        {{- $k8s_state := lookup "v1" "Secret" .Release.Namespace (include "jupyterhub.hub-secret.fullname" .) | default dict }}
        {{- if and $k8s_state (hasKey $k8s_state "JupyterHub.proxy_auth_token") }}
            {{- index $k8s_state "JupyterHub.proxy_auth_token" }}
        {{- else }}
            {{- include "jupyterhub.randHex" 64 }}
        {{- end }}
    {{- end }}
{{- end }}

{{- define "jupyterhub.config.JupyterHub.cookie_secret" -}}
    {{- if .Values.hub.cookieSecret }}
        {{- .Values.hub.cookieSecret }}
    {{- else }}
        {{- $k8s_state := lookup "v1" "Secret" .Release.Namespace (include "jupyterhub.hub-secret.fullname" .) | default dict }}
        {{- if and $k8s_state (hasKey $k8s_state "JupyterHub.cookie_secret") }}
            {{- index $k8s_state "JupyterHub.cookie_secret" }}
        {{- else }}
            {{- include "jupyterhub.randHex" 64 }}
        {{- end }}
    {{- end }}
{{- end }}

{{- define "jupyterhub.config.CryptKeeper.keys" -}}
    {{- if .Values.hub.config.CryptKeeper }}
        {{- .Values.hub.config.CryptKeeper.keys | join ";" }}
    {{- else }}
        {{- $k8s_state := lookup "v1" "Secret" .Release.Namespace (include "jupyterhub.hub-secret.fullname" .) | default dict }}
        {{- if and $k8s_state (hasKey $k8s_state "CryptKeeper.keys") }}
            {{- index $k8s_state "CryptKeeper.keys" }}
        {{- else }}
            {{- include "jupyterhub.randHex" 64 }}
        {{- end }}
    {{- end }}
{{- end }}
