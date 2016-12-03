var yourConn;
var stream;
var name;
var connectedUser;

$(document).ready(function () {

        window.history.replaceState("slack call ", "slack call ", "/call/" + roomname);
        var socket = new io.Socket(document.domain, {reconnection: true});

        userAuteticated();
        initView();


        socket.connect();

        socket.on('connect', function () {

            socket.subscribe(roomname);
            if (action == "created") {
                socket.send({action: "call", user_from: userlogged, user_to: usercall, room: roomname});
            }
            else if (action == "joined") {
                socket.send({action: "callaccept", user_from: userlogged, room: roomname});
            }


        });

        socket.on('message', onmessage);
        socket.on('disconnect', function () {
            console.log(" disconnect")
        });
        var localVideo = $('#localVideo');
        var remoteVideo = $('#remoteVideo');

        function onmessage(msg) {


            switch (msg.action) {

                //when somebody wants to call us
                case "call_begin":
                    Begin();
                    Offer(msg);
                    break;
                case "call_decline":
                    alert("se fue");
                    break;
                case "offer":
                    handleOffer(msg);
                    break;
                case "answer":
                    handleAnswer(msg);
                    break;
                //when a remote peer sends an ice candidate to us
                case "candidate":
                    handleCandidate(data.candidate);
                    break;
                case "leave":
                    handleLeave();
                    break;
                default:
                    break;
            }
        };

        function hasUserMedia() {
            //check if the browser supports the WebRTC
            return !!(navigator.getUserMedia || navigator.webkitGetUserMedia ||
            navigator.mediaDevices.getUserMedia);
        }


        function Begin() {
            updateView();


            //**********************
            //Starting a peer connection
            //**********************
            if (hasUserMedia()) {
                navigator.getMedia = (navigator.getUserMedia ||
                navigator.webkitGetUserMedia ||
                navigator.mozGetUserMedia ||
                navigator.msGetUserMedia);
                //getting local audio stream

                if (navigator.webkitGetUserMedia) {
                    navigator.mediaDevices.getUserMedia({video: false, audio: true}).then(function (myStream) {
                        stream = myStream;

                        //displaying local audio stream on the page
                        localAudio.src = window.URL.createObjectURL(stream);

                        //using Google public stun server
                        var configuration = {
                            "iceServers": [{"url": "stun:stun2.1.google.com:19302"}]
                        };


                        if (navigator.webkitGetUserMedia) {
                            yourConn = new webkitRTCPeerConnection(null);
                        }

                        // setup stream listening
                        yourConn.addStream(stream);

                        //when a remote user adds stream to the peer connection, we display it
                        yourConn.onaddstream = function (e) {
                            remoteAudio.src = window.URL.createObjectURL(e.stream);
                        };

                        // Setup ice handling
                        yourConn.onicecandidate = function (event) {
                            if (event.candidate) {
                                socket.send({
                                    type: "candidate",
                                    candidate: event.candidate
                                });
                            }
                        };

                    }).catch(function (error) {
                        console.log(error);
                    });
                }
                else {
                    navigator.getMedia({video: false, audio: true},
                        function (myStream) {
                            stream = myStream;

                            //displaying local audio stream on the page
                            localAudio.src = window.URL.createObjectURL(stream);

                            //using Google public stun server
                            var configuration = {
                                "iceServers": [{"url": "stun:stun2.1.google.com:19302"}]
                            };

                            yourConn = new RTCPeerConnection(null);

                            // setup stream listening
                            yourConn.addStream(stream);

                            //when a remote user adds stream to the peer connection, we display it
                            yourConn.onaddstream = function (e) {
                                remoteAudio.src = window.URL.createObjectURL(e.stream);
                            };

                            // Setup ice handling
                            yourConn.onicecandidate = function (event) {
                                if (event.candidate) {
                                    socket.send({
                                        type: "candidate",
                                        candidate: event.candidate
                                    });
                                }
                            };

                        },
                        function (error) {
                            console.log(error);
                        });
                }

            }

        }


        function Offer(data) {

            members(data.users);
            if (data.length > 0) {



                // create an offer
                yourConn.createOffer(function (offer) {
                    socket.send({
                        type: "offer",
                        offer: offer,
                        user_from: userlogged,
                        room: data.room
                    });

                    yourConn.setLocalDescription(offer);
                }, function (error) {
                    alert("Error when creating an offer");
                });

            }
        }


//when somebody sends us an offer
        function handleOffer(data) {
            members(data.users);

            connectedUser = name;
            yourConn.setRemoteDescription(new RTCSessionDescription(data.offer));

            //create an answer to an offer
            yourConn.createAnswer(function (answer) {
                yourConn.setLocalDescription(answer);

                socket.send({
                    type: "answer",
                    answer: answer,
                    user_from: userlogged,
                    user_to: data.user_from,
                    room: data.room
                });

            }, function (error) {
                alert("Error when creating an answer");
            });
        };

//when we got an answer from a remote user
        function handleAnswer(data) {
            members(data.users);
            yourConn.setRemoteDescription(new RTCSessionDescription(data.answer));
        };

//when we got an ice candidate from a remote user
        function handleCandidate(candidate) {
            yourConn.addIceCandidate(new RTCIceCandidate(candidate));
        };

//hang up
//     hangUpBtn.addEventListener("click", function () {
//
//         socket.send({
//             type: "leave"
//         });
//
//         handleLeave();
//     });

        function handleLeave() {
            connectedUser = null;
            remoteVideo.src = null;

            yourConn.close();
            yourConn.onicecandidate = null;
            yourConn.onaddstream = null;
            window.location.href = window.location.href;
        };


    }
);
var userAuteticated = function () {


    var avatar = "";
    if (image.length) {
        avatar = "url('/media/" + image + "')";
    }
    else {
        avatar = "url('/static/images/ava_0022-48.png')";
    }
    $('.participant .member_preview_link').css("background-image", avatar);


};
var members = function (members) {

    var participants = $("#participants");
    participants.empty();
    $.each(members, function (indes, item) {
        var avatar = "";
        if (item.user.username != userlogged) {
            if (item.image.length) {
                avatar = "url('" + item.image + "')";
            }
            else {
                avatar = "url('/static/images/ava_0022-48.png')";
            }
            var image = '<div class="member member_preview_link member_image thumb_48"' +
                ' style="background-image:' + avatar + '" ></div>'
            participants.append(item_participan(avatar, item.user.username));
        }
    });


};
var updateView = function () {

    var spinner = $(".spinner");
    spinner.hide()


};

window.request = function (urlSend, typeRequest, dataType, dataSend, doneFunction, errorFunction, type) {
    $('#convo_loading_indicator').show();
    if (type == 'file') {
        $.ajax({
            type: typeRequest,
            url: urlSend,
            data: dataSend,
            cache: false,
            contentType: false,
            processData: false,
            dataType: dataType,
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            success: doneFunction,
            error: errorFunction,
            complete: function () {
                $('#convo_loading_indicator').hide();
            }
        });
    } else {
        $.ajax({
            type: typeRequest,
            url: urlSend,
            data: dataSend,
            dataType: dataType,
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            success: doneFunction,
            error: errorFunction,
            complete: function () {
                $('#convo_loading_indicator').hide();
            }
        });
    }
};
window.getCookie = function (c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
};

var initView = function () {
    var clicked, muted = false;
    $("#calls_conference_content").append(calls_popover_invite());
    $("#calls_conference_content").append(calls_popover_settings());
    $("#calls_conference_content").append(calls_emoji_panel());
    $('#invite_icon').on('click', function () {
        if (!clicked) {
            $(this).addClass('active');
            $('.invite_menu').addClass('show');
            clicked = true;
        }
        else {
            $(this).removeClass('active');
            $('.invite_menu').removeClass('show');
            clicked = false;
        }

    });
    $('#settings_icon').on('click', function () {

        if (!clicked) {
            $(this).addClass('active');
            clicked = true;
            $('.settings_menu').addClass('show');

        }
        else {
            $(this).removeClass('active');
            $('.settings_menu').removeClass('show');
            clicked = false;

        }

    });
    $('#emoji_icon').on('click', function () {

        if (!clicked) {
            $(this).addClass('active');
            clicked = true;
            $('.emoji_panel').addClass('show');

        }
        else {
            $(this).removeClass('active');
            $('.emoji_panel').removeClass('show');
            clicked = false;

        }

    });
    $('#mute_audio').on('click', function () {

        if (!muted) {
            $(this).addClass('muted');
            muted = true;


        }
        else {
            $(this).removeClass('muted');
            muted = false;

        }

    });

};