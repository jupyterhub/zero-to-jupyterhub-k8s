{{- /*
  jupyterhub.userTolerations
    Lists the tolerations for node taints that the user pods should have
*/}}
{{- define "jupyterhub.userTolerations" -}}
- key: hub.jupyter.org_dedicated
  operator: Equal
  value: user
  effect: NoSchedule
- key: hub.jupyter.org/dedicated
  operator: Equal
  value: user
  effect: NoSchedule
{{- if .Values.singleuser.extraTolerations }}
{{- .Values.singleuser.extraTolerations | toYaml | trimSuffix "\n" | nindent 0 }}
{{- end }}
{{- end }}



{{- define "jupyterhub.userNodeAffinityRequired" -}}
{{- if eq .Values.scheduling.userPods.nodeAffinity.matchNodePurpose "require" -}}
- matchExpressions:
  - key: hub.jupyter.org/node-purpose
    operator: In
    values: [user]
{{- end }}
{{- if .Values.singleuser.extraNodeAffinity.required }}
{{- .Values.singleuser.extraNodeAffinity.required | toYaml | trimSuffix "\n" | nindent 0 }}
{{- end }}
{{- end }}

{{- define "jupyterhub.userNodeAffinityPreferred" -}}
{{- if eq .Values.scheduling.userPods.nodeAffinity.matchNodePurpose "prefer" -}}
- weight: 100
  preference:
    matchExpressions:
      - key: hub.jupyter.org/node-purpose
        operator: In
        values: [user]
{{- end }}
{{- if .Values.singleuser.extraNodeAffinity.preferred }}
{{- .Values.singleuser.extraNodeAffinity.preferred | toYaml | trimSuffix "\n" | nindent 0 }}
{{- end }}
{{- end }}

{{- define "jupyterhub.userPodAffinityRequired" -}}
{{- if .Values.singleuser.extraPodAffinity.required -}}
{{ .Values.singleuser.extraPodAffinity.required | toYaml | trimSuffix "\n" }}
{{- end }}
{{- end }}

{{- define "jupyterhub.userPodAffinityPreferred" -}}
{{- if .Values.singleuser.extraPodAffinity.preferred -}}
{{ .Values.singleuser.extraPodAffinity.preferred | toYaml | trimSuffix "\n" }}
{{- end }}
{{- end }}

{{- define "jupyterhub.userPodAntiAffinityRequired" -}}
{{- if .Values.singleuser.extraPodAntiAffinity.required -}}
{{ .Values.singleuser.extraPodAntiAffinity.required | toYaml | trimSuffix "\n" }}
{{- end }}
{{- end }}

{{- define "jupyterhub.userPodAntiAffinityPreferred" -}}
{{- if .Values.singleuser.extraPodAntiAffinity.preferred -}}
{{ .Values.singleuser.extraPodAntiAffinity.preferred | toYaml | trimSuffix "\n" }}
{{- end }}
{{- end }}



{{- /*
  jupyterhub.userAffinity:
    It is used by user-placeholder to set the same affinity on them as the
    spawned user pods spawned by kubespawner.
*/}}
{{- define "jupyterhub.userAffinity" -}}

{{- $dummy := set . "nodeAffinityRequired" (include "jupyterhub.userNodeAffinityRequired" .) -}}
{{- $dummy := set . "podAffinityRequired" (include "jupyterhub.userPodAffinityRequired" .) -}}
{{- $dummy := set . "podAntiAffinityRequired" (include "jupyterhub.userPodAntiAffinityRequired" .) -}}
{{- $dummy := set . "nodeAffinityPreferred" (include "jupyterhub.userNodeAffinityPreferred" .) -}}
{{- $dummy := set . "podAffinityPreferred" (include "jupyterhub.userPodAffinityPreferred" .) -}}
{{- $dummy := set . "podAntiAffinityPreferred" (include "jupyterhub.userPodAntiAffinityPreferred" .) -}}
{{- $dummy := set . "hasNodeAffinity" (or .nodeAffinityRequired .nodeAffinityPreferred) -}}
{{- $dummy := set . "hasPodAffinity" (or .podAffinityRequired .podAffinityPreferred) -}}
{{- $dummy := set . "hasPodAntiAffinity" (or .podAntiAffinityRequired .podAntiAffinityPreferred) -}}

{{- if .hasNodeAffinity -}}
nodeAffinity:
  {{- if .nodeAffinityRequired }}
  requiredDuringSchedulingIgnoredDuringExecution:
    nodeSelectorTerms:
      {{- .nodeAffinityRequired | nindent 6 }}
  {{- end }}

  {{- if .nodeAffinityPreferred }}
  preferredDuringSchedulingIgnoredDuringExecution:
    {{- .nodeAffinityPreferred | nindent 4 }}
  {{- end }}
{{- end }}

{{- if .hasPodAffinity }}
podAffinity:
  {{- if .podAffinityRequired }}
  requiredDuringSchedulingIgnoredDuringExecution:
    {{- .podAffinityRequired | nindent 4 }}
  {{- end }}

  {{- if .podAffinityPreferred }}
  preferredDuringSchedulingIgnoredDuringExecution:
    {{- .podAffinityPreferred | nindent 4 }}
  {{- end }}
{{- end }}

{{- if .hasPodAntiAffinity }}
podAntiAffinity:
  {{- if .podAntiAffinityRequired }}
  requiredDuringSchedulingIgnoredDuringExecution:
    {{- .podAntiAffinityRequired | nindent 4 }}
  {{- end }}

  {{- if .podAntiAffinityPreferred }}
  preferredDuringSchedulingIgnoredDuringExecution:
    {{- .podAntiAffinityPreferred | nindent 4 }}
  {{- end }}
{{- end }}

{{- end }}



{{- define "jupyterhub.coreAffinity" -}}
{{- $require := eq .Values.scheduling.corePods.nodeAffinity.matchNodePurpose "require" -}}
{{- $prefer := eq .Values.scheduling.corePods.nodeAffinity.matchNodePurpose "prefer" -}}
{{- if or $require $prefer -}}
affinity:
  nodeAffinity:
    {{- if $require }}
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
          - key: hub.jupyter.org/node-purpose
            operator: In
            values: [core]
    {{- end }}
    {{- if $prefer }}
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        preference:
          matchExpressions:
            - key: hub.jupyter.org/node-purpose
              operator: In
              values: [core]
    {{- end }}
{{- end }}
{{- end }}
