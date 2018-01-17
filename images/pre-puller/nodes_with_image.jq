# Expects an argument, $image, containing the imagespec to look for
# Outputs a JSON list of node names that contain that image
def image_exists(node):
    [node.status.images[].names[] | contains($image)] | any
;

[.items[] | select(image_exists(.)) | .metadata.name]
