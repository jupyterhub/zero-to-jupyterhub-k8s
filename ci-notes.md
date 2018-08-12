1. Create a tests directory in the jupyterhub folder with tests
   - https://github.com/jupyterhub/binderhub/tree/master/binderhub/tests
   - https://nbviewer.jupyter.org/gist/minrk/f01de9d7295ed58c4b0dda183ff7209a
   - http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/docs/rest-api.yml
   - To make a request:
     
     0. send apiToken in authorization header
     1. create the user
     2. spawn the server
     3. wait for the server
   
   - Add (Generate best!) a service.tests.apiToken to a config.yaml we pass

    hub:
    services:
      tests:
        admin: true
        apiToken: "0cc05feaefeeb29179e924ffc6d3886ffacf0d1a28ab225f5c210436ffc5cfd5"

     

2. Run from the end of test.sh

pytest -vsx

---

Remove the .sh file ending