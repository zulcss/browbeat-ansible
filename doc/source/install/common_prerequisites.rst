Prerequisites
-------------

Before you install and configure the browbeat service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``browbeat`` database:

     .. code-block:: none

        CREATE DATABASE browbeat;

   * Grant proper access to the ``browbeat`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON browbeat.* TO 'browbeat'@'localhost' \
          IDENTIFIED BY 'BROWBEAT_DBPASS';
        GRANT ALL PRIVILEGES ON browbeat.* TO 'browbeat'@'%' \
          IDENTIFIED BY 'BROWBEAT_DBPASS';

     Replace ``BROWBEAT_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``browbeat`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt browbeat

   * Add the ``admin`` role to the ``browbeat`` user:

     .. code-block:: console

        $ openstack role add --project service --user browbeat admin

   * Create the browbeat service entities:

     .. code-block:: console

        $ openstack service create --name browbeat --description "browbeat" browbeat

#. Create the browbeat service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        browbeat public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        browbeat internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        browbeat admin http://controller:XXXX/vY/%\(tenant_id\)s
