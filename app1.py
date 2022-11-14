<head>
    <!-- Required meta tags -->
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <title>Robot Webpage</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=default"></script>
    <style>
        /* 
         * Always set the map height explicitly to define the size of the div element
         * that contains the map. 
         */
        #map {
          height: 100%;
        }
        
        /* 
         * Optional: Makes the sample page fill the window. 
         */
        html,
        body {
          height: 100%;
          margin: 0;
          padding: 0;
        }
        
        .custom-map-control-button {
          background-color: #fff;
          border: 0;
          border-radius: 2px;
          box-shadow: 0 1px 4px -1px rgba(0, 0, 0, 0.3);
          margin: 10px;
          padding: 0 0.5em;
          font: 400 18px Roboto, Arial, sans-serif;
          overflow: hidden;
          height: 40px;
          cursor: pointer;
        }
        .custom-map-control-button:hover {
          background: rgb(235, 235, 235);
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">ROBOT UI</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
        </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">About Us</a>
                    </li>
                </ul>
                <form class="d-flex">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>
            </div>
        </div>
    </nav>
    <center>
    <section>
        <div class="container-fluid" style="padding-top: 100px;">
            <h1>Welcome to TSU VR-Lab ROS User Interface</h1>
            <p style="font-size: 24px; font-weight: bold; color: #51995d;">Connection status:
                <span id="status"></span>
            </p>
    </section>
    
       <!-- INFO -->
       <section style="margin-top: 10px;"> 
        <div class="row my-4" >
            <div class="col-md-2" ></div>
            <div class="col-md-8">
                <div class="alert alert-success">
                    <h4 class="alert-heading">How it works</h4>
                    <p>Set speed using a slider</p>
                    <p>Use joystick to move any direction</p> 
                     <p>Or Use keyboard W (up) | A(left) | S(down) | D(right) to move </p>
                </div>
            </div>
            <div class="col-md-2"></div>
        </div>
    </section>

    <!-- SPEED -->
    <div class="row">
        <div class="col-md-4"></div>
        <div class=" col-md-4">
            <label for="robot-speed">
                <strong>Robot speed</strong>
            </label>
            <input type="range" min="15" max="80" class="custom-range" id="robot-speed">
        </div>
        <div class="col-md-4"></div>
    </div>
    <section>
        <div class="container" style="padding-top: 40px;">
            <div class="row">
                <div class="col">
                    <section>
                        <!-- VIDEO -->
                        <img class="p-1 bg-dark" src="stream.mjpg" width="640" height="480">
                    </section>
                </div>
                <div class="col">
                    <section>
                        <!-- JOYSTICK -->
                        <div id="joystick" style="width: 210px; margin-top: 100px; position: relative;"></div>
                    </section>
                </div>
            </div>
        </div>
    </section>
    <section style="margin-top: 300px;"></section>
 
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous">
    </script>
    <script type="text/javascript" src="https://static.robotwebtools.org/roslibjs/current/roslib.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/nipplejs/0.7.3/nipplejs.js"></script>
    <script src="https://static.robotwebtools.org/keyboardteleopjs/current/keyboardteleop.min.js"></script>
    <script type="text/javascript" src="app.js"></script>
        <script>
            var twist;
            var cmdVel;
            var publishImmidiately = true;
            var robot_IP;
            var manager;
            var teleop;
            var ros;
            function moveAction(linear, angular) {
                if (linear !== undefined && angular !== undefined) {
                    twist.linear.x = linear;
                    twist.angular.z = angular;
                } else {
                    twist.linear.x = 0;
                    twist.angular.z = 0;
                }
                cmdVel.publish(twist);
            }
            function initVelocityPublisher() {
                // Init message with zero values.
                twist = new ROSLIB.Message({
                    linear: {
                        x: 0,
                        y: 0,
                        z: 0
                    },
                    angular: {
                        x: 0,
                        y: 0,
                        z: 0
                    }
                });
                // Init topic object
                cmdVel = new ROSLIB.Topic({
                    ros: ros,
                    name: '/cmd_vel',
                    messageType: 'geometry_msgs/Twist'
                });
                // Register publisher within ROS system
                cmdVel.advertise();
            }
            function initTeleopKeyboard() {
                // Use w, s, a, d keys to drive your robot
                // Check if keyboard controller was aready created
                if (teleop == null) {
                    // Initialize the teleop.
                    teleop = new KEYBOARDTELEOP.Teleop({
                        ros: ros,
                        topic: '/cmd_vel'
                    });
                }
                // Add event listener for slider moves
                robotSpeedRange = document.getElementById("robot-speed");
                robotSpeedRange.oninput = function () {
                    teleop.scale = robotSpeedRange.value / 100
                }
            }
            function createJoystick() {
                // Check if joystick was aready created
                if (manager == null) {
                    joystickContainer = document.getElementById('joystick');
                    // joystck configuration, if you want to adjust joystick, refer to:
                    // https://yoannmoinet.github.io/nipplejs/
                    var options = {
                        zone: joystickContainer,
                        position: { left: 50 + '%', top: 105 + 'px' },
                        mode: 'static',
                        size: 200,
                        color: '#00853c',
                        restJoystick: true
                    };
                    manager = nipplejs.create(options);
                    // event listener for joystick move
                    manager.on('move', function (evt, nipple) {
                        // nipplejs returns direction is screen coordiantes
                        // we need to rotate it, that dragging towards screen top will move robot forward
                        var direction = nipple.angle.degree - 90;
                        if (direction > 180) {
                            direction = -(450 - nipple.angle.degree);
                        }
                        // convert angles to radians and scale linear and angular speed
                        // adjust if youwant robot to drvie faster or slower
                        var lin = Math.cos(direction / 57.29) * nipple.distance * 0.005;
                        var ang = Math.sin(direction / 57.29) * nipple.distance * 0.05;
                        // nipplejs is triggering events when joystic moves each pixel
                        // we need delay between consecutive messege publications to
                        // prevent system from being flooded by messages
                        // events triggered earlier than 50ms after last publication will be dropped
                        if (publishImmidiately) {
                            publishImmidiately = false;
                            moveAction(lin, ang);
                            setTimeout(function () {
                                publishImmidiately = true;
                            }, 50);
                        }
                    });
                    // event litener for joystick release, always send stop message
                    manager.on('end', function () {
                        moveAction(0, 0);
                    });
                }
            }
            window.onload = function () {
                // determine robot address automatically
                robot_IP = location.hostname;
                // set robot address statically
                //robot_IP = "172.24.202.76";
               // // Init handle for rosbridge_websocket               
                ros = new ROSLIB.Ros({
                    url: "ws://" + robot_IP + ":9090"
                });
                ros.on('connection', function () {
                    document.getElementById("status").innerHTML = "Connected";
                });
                ros.on('error', function (error) {
                    document.getElementById("status").innerHTML = "Error";
                });
                ros.on('close', function () {
                    document.getElementById("status").innerHTML = "Closed";
                });
                initVelocityPublisher();
                createJoystick();
                initTeleopKeyboard();
            }
	    </script>
  </body>
</html>
