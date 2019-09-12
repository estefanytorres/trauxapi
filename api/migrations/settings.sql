-----------------------------------------------------------------------------------------------------------------------
----------------------------------------------  api_messageset  -------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
DELETE FROM api_messageset;

INSERT INTO api_messageset (message_set, title, description) VALUES (1000, 'Comunicaciones', 'Catálogo de comunicaciones de la applicacion');

-----------------------------------------------------------------------------------------------------------------------
---------------------------------------------  api_messagecatalog  ----------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
DELETE FROM api_messagecatalog;

INSERT INTO api_messagecatalog (id, message_nbr, description, message, message_set_id) VALUES (16, 1, 'Correo Contacto desde la web - subject (webmaster)', 'Solicitud de contacto desde la web', 1000);
INSERT INTO api_messagecatalog (id, message_nbr, description, message, message_set_id) VALUES (17, 2, 'Correo Contacto desde la web - body (webmaster)', '<p>
<b>Nombres:</b> {}<br>
<b>Empresa:</b> {}<br>
<b>Correo:</b> {}<br>
<b>Telefono:</b> {}<br>
</p>
<p>{}</p>', 1000);
INSERT INTO api_messagecatalog (id, message_nbr, description, message, message_set_id) VALUES (18, 3, 'Correo Descarga de demo desde la web - subject (webmaster)', 'Descarga de traux versión DEMO desde la web', 1000);
INSERT INTO api_messagecatalog (id, message_nbr, description, message, message_set_id) VALUES (19, 4, 'Correo Descarga de demo desde la web - body (webmaster)', '<p>
<b>Nombres:</b> {}<br>
<b>Empresa:</b> {}<br>
<b>Correo:</b> {}<br>
<b>Telefono:</b> {}<br>
</p>', 1000);
INSERT INTO api_messagecatalog (id, message_nbr, description, message, message_set_id) VALUES (20, 5, 'Correo Descarga de demo desde la web - subject (customer)', 'Tu trauxerp version DEMO!', 1000);
INSERT INTO api_messagecatalog (id, message_nbr, description, message, message_set_id) VALUES (21, 6, 'Correo Descarga de demo desde la web - body (customer)', '<h2>Hola {}!</h2>
<p>Te felicito por iniciar tu camino hacia organizar y mejorar los procesos de negocio de tu empresa, de parte de todo el equipo traux te damos las gracias por considerarnos como opción, sabemos que hay muchos sistemas en el mercado y que quieres estar seguro que aquel que eligas este en sintonía con tus objetivos. Es por eso que nosotros ofrecemos tres meses de prueba con nuestro sistema, solo queremos ayudarte a decidir si traux es la opción correcta para tí.</p>

<p>El primer paso es descargar el sistema utilizando el siguiente link:</p>
<p><a href="{}">DESCARGA AQUÍ</a></p>

<p>Luego sigue las instrucciones que tenemos para ti en nuestro canal de <a href="https://youtu.be/lpIwWB6anjs">youtube</a></p>

<p>Si llegas a tener cualquier duda por favor comunícate con nosotros respondiento a este correo que con gusto te ayudaremos!</p>

<p>De nuevo muchas gracias,<br>
El equipo traux</p>
<img src="{}">', 1000);
INSERT INTO api_messagecatalog (id, message_nbr, description, message, message_set_id) VALUES (22, 7, 'Correo activación de usuario - subject', 'Activa tu cuenta Traux', 1000);
INSERT INTO api_messagecatalog (id, message_nbr, description, message, message_set_id) VALUES (23, 8, 'Correo activación de usuario - body', '<div style="margin: 1em auto;max-width: 600px; padding: 2em; border-radius: 10px;">
<h2>Hola {}!</h2>
<p>Para confirmar su correo electrónico, haga click en el siguiente enlace: {}</p>
<br>
<p>El equipo traux</p>
<img src="https://www.trauxerp.com/assets/logo-sinescrito.png" style="width: 150px">
</div>', 1000);
INSERT INTO api_messagecatalog (id, message_nbr, description, message, message_set_id) VALUES (24, 9, 'Correo usuario activado - subject', 'Bienvenido', 1000);
INSERT INTO api_messagecatalog (id, message_nbr, description, message, message_set_id) VALUES (25, 10, 'Correo usuario activado - body', '<div style="margin: 1em auto;max-width: 600px; padding: 2em; border-radius: 10px;">
<h2>Bienvenido(a) {}!</h2>
<p>a traves de esta comunicación hacemos de su conocimiento que su registro ha quedado almacenado con el usuario {} y la contraseña que usted especificó</p>
<br>
<p>Gracias por confiar en nosotros,</p>
<p>El equipo traux</p>
<img src="https://www.trauxerp.com/assets/logo-sinescrito.png" style="width: 150px">
</div>', 1000);