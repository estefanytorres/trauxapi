-----------------------------------------------------------------------------------------------------------------------
----------------------------------------------  api_messageset  -------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
DELETE FROM api_messageset where message_set < 2000;

INSERT INTO api_messageset (message_set, title, description) VALUES (200, 'Mensajes de éxito', 'Mensajes de la api');
INSERT INTO api_messageset (message_set, title, description) VALUES (201, 'Mensajes de creación', 'Mensajes de la api');
INSERT INTO api_messageset (message_set, title, description) VALUES (400, 'Mensajes de error', 'Errores de la api');
INSERT INTO api_messageset (message_set, title, description) VALUES (500, 'Errores del servidor', 'Errores del servidor');
INSERT INTO api_messageset (message_set, title, description) VALUES (1000, 'Comunicaciones', 'Catálogo de comunicaciones de la applicacion');

-----------------------------------------------------------------------------------------------------------------------
---------------------------------------------  api_messagecatalog  ----------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
DELETE FROM api_messagecatalog where message_set_id < 2000;

-- message_set: 200 - Mensajes de exito
---------------------------------------------------------

INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (200, 10, 'User.activate()', 'Usuario activado');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (200, 11, 'User.activate()', 'Usuario ya se encontraba activado');

INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (200, 20, 'User.email_reset_password()', 'Correo de reestablecimiento de contraseña enviado');

INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (200, 30, 'User.reset_password()', 'Contraseña reestablecida');

-- message_set: 201 - Mensajes de exito
---------------------------------------------------------

INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (201, 1, 'User.register()', 'Usuario creado con éxito, correo de activacion enviado');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (201, 2, 'User.register()', 'Usuario creado con éxito, correo de activacion enviado a la dirección registrada para la licencia ingresada');

-- message_set: 400 - Mensajes de exito error
---------------------------------------------------------

INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (400, 1, 'User.register()', 'La licencia es inválida');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (400, 2, 'User.register()', 'Nombre de usuario ya existe');

INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (400, 10, 'User.activate()', 'Token inválido');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (400, 11, 'User.activate()', 'Usuario inválido');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (400, 12, 'User.activate()', 'Parametros inválidos, parametros necesarios: [uid, token]');

INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (400, 20, 'User.email_reset_password()', 'Parametros inválidos, parametros necesarios: [username]');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (400, 21, 'User.email_reset_password()', 'Usuario inválido');

INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (400, 30, 'User.reset_password()', 'Usuario inactivo');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (400, 31, 'User.reset_password()', 'Token inválido');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (400, 32, 'User.reset_password()', 'Usuario inválido');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (400, 33, 'User.reset_password()', 'Parametros inválidos, parametros necesarios: [uid, token, password]');


-- message_set: 500 - Errores del servidor
---------------------------------------------------------

INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (500, 0, 'User.register()', 'Error inesperado al registrar el usuario');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (500, 1, 'User.register()', 'Perfil de usuario no existe');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (500, 2, 'User.register()', 'Error al generar el mensaje para el correo de activación');

INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (500, 10, 'User.activate()', 'Error inesperado al activar el usuario');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (500, 11, 'User.activate()', 'Perfil de usuario no existe');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (500, 12, 'User.activate()', 'Error al generar el mensaje para el correo de activación');

INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (500, 20, 'User.email_reset_password()', 'Error inesperado al enviar el correo de reestablecimiento de contraseña');

INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (500, 30, 'User.reset_password()', 'Error inesperado al reestablecer la contraseña');

-- message_set: 1000 - Comunicaciones
---------------------------------------------------------

INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (1000, 1, 'Correo Contacto desde la web - subject (webmaster)', 'Solicitud de contacto desde la web');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (1000, 2, 'Correo Contacto desde la web - body (webmaster)', '<p>
<b>Nombres:</b> {}<br>
<b>Empresa:</b> {}<br>
<b>Correo:</b> {}<br>
<b>Telefono:</b> {}<br>
</p>
<p>{}</p>');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (1000, 3, 'Correo Descarga de demo desde la web - subject (webmaster)', 'Descarga de traux versión DEMO desde la web');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (1000, 4, 'Correo Descarga de demo desde la web - body (webmaster)', '<p>
<b>Nombres:</b> {}<br>
<b>Empresa:</b> {}<br>
<b>Correo:</b> {}<br>
<b>Telefono:</b> {}<br>
</p>');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (1000, 5, 'Correo Descarga de demo desde la web - subject (customer)', 'Tu trauxerp version DEMO!');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (1000, 6, 'Correo Descarga de demo desde la web - body (customer)', '<h2>Hola {}!</h2>
<p>Te felicito por iniciar tu camino hacia organizar y mejorar los procesos de negocio de tu empresa, de parte de todo el equipo traux te damos las gracias por considerarnos como opción, sabemos que hay muchos sistemas en el mercado y que quieres estar seguro que aquel que eligas este en sintonía con tus objetivos. Es por eso que nosotros ofrecemos tres meses de prueba con nuestro sistema, solo queremos ayudarte a decidir si traux es la opción correcta para tí.</p>

<p>El primer paso es descargar el sistema utilizando el siguiente link:</p>
<p><a href="{}">DESCARGA AQUÍ</a></p>

<p>Luego sigue las instrucciones que tenemos para ti en nuestro canal de <a href="https://youtu.be/lpIwWB6anjs">youtube</a></p>

<p>Si llegas a tener cualquier duda por favor comunícate con nosotros respondiento a este correo que con gusto te ayudaremos!</p>

<p>De nuevo muchas gracias,<br>
El equipo traux</p>
<img src="{}">');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (1000, 7, 'Correo activación de usuario - subject', 'Activa tu cuenta Traux');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (1000, 8, 'Correo activación de usuario - body', '<div style="margin: 1em auto;max-width: 600px; padding: 2em; border-radius: 10px;">
<h2>Hola {}!</h2>
<p>Para confirmar su correo electrónico, haga click en el siguiente enlace: {}</p>
<br>
<p>El equipo traux</p>
<img src="https://www.trauxerp.com/assets/logo-sinescrito.png" style="width: 150px">
</div>');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (1000, 9, 'Correo usuario activado - subject', 'Bienvenido');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (1000, 10, 'Correo usuario activado - body', '<div style="margin: 1em auto;max-width: 600px; padding: 2em; border-radius: 10px;">
<h2>Bienvenido(a) {}!</h2>
<p>A través de esta comunicación hacemos de su conocimiento que su registro ha quedado almacenado con el usuario {} y la contraseña que usted especificó</p>
<br>
<p>Gracias por confiar en nosotros,
<br>
El equipo traux</p>
<img src="https://www.trauxerp.com/assets/logo-sinescrito.png" style="width: 150px">
</div>');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (1000, 11, 'Correo olvidé mi contraseña - subject', 'Asistencia de contraseña traux');
INSERT INTO api_messagecatalog (message_set_id, message_nbr, description, message) VALUES (1000, 12, 'Correo olvidé mi contraseña - body',
'<div style="margin: 1em auto;max-width: 600px; padding: 2em; border-radius: 10px;">
<h2>Hola {}!</h2>
<p>Para reestablecer su contraseña, haga click en el siguiente enlace: {}</p>
<br>
<p>El equipo traux</p>
<img src="https://www.trauxerp.com/assets/logo-sinescrito.png" style="width: 150px">
</div>');
