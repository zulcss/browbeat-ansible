2. Edit the ``/etc/browbeat/browbeat.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://browbeat:BROWBEAT_DBPASS@controller/browbeat
