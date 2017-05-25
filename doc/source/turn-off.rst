Turning it all off
==================

1. If you want to stop these resources from running, you’ll need to tell google
   cloud to explicitly turn off the cluster that we have created. This is
   possible `from the web console <https://console.cloud.google.com>`_ if you
   click on the hamburger menu (the 3 horizontal lines) in the top left, and
   then click on the ``Container Engine`` section (see figure). Click on the
   container you wish to delete and press the “delete” button.

   .. image:: _static/images/container_engine_location.jpg
      :height: 600px

   .. note::

      Alternatively, you can run the following command to delete the cluster of your choice.

      ``gcloud container clusters delete YOUR_CLUSTER --zone=YOUR_ZONE``

2. Now your cluster resources should be gone after a few moments - double check this or you will continue to incur charges!
