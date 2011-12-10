django-fab-deployment - A collection of fab files for ubuntu/debian + django websites.
=======================================================================================

I found myself repeating the same scripts over and over again, so I decided to do something about it.
Current the library is very rough, but should work for now.  Before you use it, take a look at the source
to make sure it's not going to do anything unexpected for your particular use case.


Installation
--------------
1. Install source::

   pip install https://github.com/samdolan/django-fab-deployment

2. Ensure succesfull installation::

   python -c "import fab_deploy"


Current Supported Stack
-------------------------
 
* Ubuntu 10.04
* virtualenv + virtualenvwrapper
* Django
* uWSGI
* nginx
* supervisor
* postgres 9.1

Integration with your fabfile
--------------------------------------------

Copy over the example configuration file in fab_deploy/fabfile.yaml.tmpl
and update it to suit your project. 

**NOTE** The db and web can be on the same machine, but we'll still use tcp communication.

In your fabfile.py/fabfile/__init__.py file. add the following::

    from fabric.api import *

    # Get all of the tasks defined by the fabric library
    # You can narrow this down to by importing them seperately, so
    # they don't pollute the fab list.
    from fab_deploy.contrib import *
    from fab_deploy.contrib.conf import set_yaml_config
    from fab_deploy.contrib.roles import set_role_group

    # change to whatever you named your yaml config to
    set_yaml_config(os.path.join(os.path.dirname(__file__), 'fabfile.yaml'))

    @task
    def dev():
        # Or whatever was defined in your servers directive in the yaml file.
        # I suggest creating a new task for each of these.
        set_role_group('dev')

Run ``fab -l`` and you should see a list of different operations.  Some examples:

Setup a dev server::

    fab dev servers.setup

To upgrade the dev server::
    
    fab dev servers.update


Contributing
--------------
Feel free to send pull requests with new libraries/suggestions.  I'm planning to slowly transfer this
into a highly configurable fabric system. Also, if you see any issues with how the configuration is setup
don't hesitate to open an issue.

Liscence
-----------
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

