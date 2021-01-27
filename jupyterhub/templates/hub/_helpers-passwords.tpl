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

    In practice, it generates up to 25 randAlphaNum strings
    that are filtered from non-hex characters and augmented
    to the resulting string that is finally trimmed down. We
    do it multiple times as on average we filter out 4/15 of
    the characters.
*/}}
{{- define "jupyterhub.randHex" -}}
    {{- $result := "" }}
    {{- $context := . }}
    {{- range $i := until 26 }}{{- /* 1-25 */}}
        {{- if lt (len $result) $context }}
            {{- $rand_anum_string := randAlphaNum $context }}
            {{- $rand_anum_list := $rand_anum_string | splitList "" }}
            {{- $rand_hex_list := without $rand_anum_list "g" "h" "i" "j" "k" "l" "m" "n" "o" "p" "q" "r" "s" "t" "u" "v" "w" "x" "y" "z" "A" "B" "C" "D" "E" "F" "G" "H" "I" "J" "K" "L" "M" "N" "O" "P" "Q" "R" "S" "T" "U" "V" "W" "X" "Y" "Z" }}
            {{- $rand_hex_string := join "" $rand_hex_list }}
            {{- $result = print $result $rand_hex_string }}
        {{- end }}
    {{- end }}
    {{- /* We shuffle the generated hex numbers for good measure */}}
    {{- $result | trunc $context | shuffle }}
{{- end }}

{{- define "jupyterhub.config.JupyterHub.proxy_auth_token" -}}
    {{- if .Values.proxy.secretToken }}
        {{- .Values.proxy.secretToken }}
    {{- else }}
        {{- $k8s_state := lookup "v1" "Secret" .Release.Namespace (include "jupyterhub.hub-secret.fullname" .) | default (dict "data" (dict)) }}
        {{- if hasKey $k8s_state.data "JupyterHub.proxy_auth_token" }}
            {{- index $k8s_state.data "JupyterHub.proxy_auth_token" | b64dec }}
        {{- else }}
            {{- include "jupyterhub.randHex" 64 }}
        {{- end }}
    {{- end }}
{{- end }}

{{- define "jupyterhub.config.JupyterHub.cookie_secret" -}}
    {{- if .Values.hub.cookieSecret }}
        {{- .Values.hub.cookieSecret }}
    {{- else }}
        {{- $k8s_state := lookup "v1" "Secret" .Release.Namespace (include "jupyterhub.hub-secret.fullname" .) | default (dict "data" (dict)) }}
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
        {{- $k8s_state := lookup "v1" "Secret" .Release.Namespace (include "jupyterhub.hub-secret.fullname" .) | default (dict "data" (dict)) }}
        {{- if hasKey $k8s_state.data "CryptKeeper.keys" }}
            {{- index $k8s_state.data "CryptKeeper.keys" | b64dec }}
        {{- else }}
            {{- include "jupyterhub.randHex" 64 }}
        {{- end }}
    {{- end }}
{{- end }}
