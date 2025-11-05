/*

A handheld camera case with a turret mount, for Raspberry Pi Zero
Jenny List 2025
CC-BY-SA 4.0

*/

// Requirws thw following two libraries
include <./jennys-rectangular-project-box.scad>
include <./m12-turret-camera.scad>

//Main box with camera mount
module zeroCameraBox(){
    difference(){
        projectBox(100,75,30,3,1,1.25); //the box itself    
        translate([50,37.5,0]){ //cut-outs for Zero mounting holes
            translate([-29,-11.5,0]) cylinder(5,1.25,1.25,$fn=90);
            translate([29,-11.5,0]) cylinder(5,1.25,1.25,$fn=90);
            translate([-29,11.5,0]) cylinder(5,1.25,1.25,$fn=90);
            translate([29,11.5,0]) cylinder(5,1.25,1.25,$fn=90);
        }
        translate([50,0,20]){ 
            cube([65,5,30],true); //cut-out for cables
        }
        translate([50,37.5,0]) cube([48.5,35.5,5],true); //cut-out for Pimoroni screen
        translate([50,37.5,0]) cube([56,17,5],true); //cut-out for Pimoroni buttons
    }
}
//Lid for box with Pimoroni sreeen and Zero mount
module zeroCameraLid(){
    difference(){
        projectBoxLid(100,75,30,3,1,1.25);
        translate([15,2.5,0]){ 
            cube([70,70,70]); //cut-out for turret assembly
        }
    }
    translate([50,37.5,2]) rotate([180,0,0]) TurretHolder();
}

//Four stand-offs for between the Pimoroni board and the Pi
module zeroCameraStandoffs(){
    for(i=[0:3]){
        translate([i*7,0,0]){
            difference(){
                cylinder(9,2.75,2.75,$fn=6);
                cylinder(9,1,1);
            }
        }
    }
    translate([-1,2.38,0]) cube([22.5,1,0.25]); //printing supports
    translate([-1,-3.38,0]) cube([22.5,1,0.25]);
}

//Main box with Pi and Pimoroni screen mounting.
zeroCameraBox();
//Lid with turret mount
translate([0,160,2]) rotate([180,0,0]) zeroCameraLid();
//Four stand-offs for mounting the Raspberry Pi Zero
translate([40,35,0]) zeroCameraStandoffs();

//You will also need the turret itself and the camera back plate.
//These can be found in m12-turret-camera.scad