{{- /*
Renders the kube-scheduler's image based on .Values.scheduling.userScheduler.name and
optionally on .Values.scheduling.userScheduler.tag. The default tag is set to the clusters
kubernetes version.
*/}}
{{- define "jupyterhub.scheduler.image" -}}
{{- $name := .Values.scheduling.userScheduler.image.name -}}
{{- $valuesVersion := .Values.scheduling.userScheduler.image.tag -}}
{{- $clusterVersion := (split "-" .Capabilities.KubeVersion.GitVersion)._0 -}}
{{- $tag := $valuesVersion | default $clusterVersion -}}
{{ $name }}:{{ $tag }}
{{- end }}
