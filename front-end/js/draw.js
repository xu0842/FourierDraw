
var pillar=new Array();//class Pillar(canvas, x1, y1, x2, y2, width, color){}
var dot=new Array();//class Dot(canvas, x, y, r, color){}

function draw(){
    requestAnimationFrame(draw);
    let ctx= canvas.getContext('2d');
    ctx.clearRect(0,0,canvas.width,canvas.height);
    if(!trace.length){
        for(let c=0;c<pillar.length;c++){
            pillar[c].draw();
        }
        for(let a=0;a<dot.length;a++){
            dot[a].draw();
        }
    }
    else{//if(!trace.length)
        
        if(pillar.length>1){
            for(let k=0;k<pillar.length;k++){
                pillar[k].rota();
                if(k<pillar.length-1){
                    pointmove(pillar[k+1],pillar[k].x2,pillar[k].y2);
                }
            }
        }	
        else if(pillar.length==1) 
            pillar[0].rota();//*/
        for(let a=0;a<pillar.length;a++){
           //document.getElementById("P").innerHTML=pillar[a].x1+","+pillar[a].x2;
            pillar[a].draw();
            if(drawcircle.checked&&a<=pillar.length/2) 
                circle(canvas,pillar[a].x1,pillar[a].y1,pillar[a].len,pillar[a].color,0.4);
        }//*/

        
       
        if(pillar.length){ //绘制点轨迹
            dot[dot.length]=new Dot(canvas,pillar[pillar.length-1].x2,pillar[pillar.length-1].y2,1.5,"rgba(255,255,0,0.5)");
            if(dot.length>=1960){
                dot.shift();
            }
            for(let j=0;j<dot.length;j++){
                dot[j].color="rgba("+(127*Math.sin(2*Math.PI/dot.length*(j+dot.length/3))+127)+","+(100*Math.sin(2*Math.PI/dot.length*j)+100)+","+(127*Math.sin(2*Math.PI/dot.length*(j-dot.length/3))+127)+","+(j/120+0.3)+")";
                //三相彩虹色
                dot[j].draw();
            }
        }
    }
}


function setpaint(width,a,b,s){
    pillar.length=0;
    dot.length=0;
    for(let i=0;i<trace.length-1;i+=1){
        pillar[i]=new Pillar(canvas,s*trace[i][0]+a,s*trace[i][1]+b,s*trace[i+1][0]+a,s*trace[i+1][1]+b,width,"rgba(160,160,240,0.7)");
        let w=i+1;
        var t=25;
        pillar[i].dr=Math.PI*Math.pow(-1,w)*Math.round(w/2+0.2)/4/t;
    }//950&12
}

function pointmove(p,x,y){ //多杆联接
    if(p.x2>=p.x1){
        p.x1=x-p.axis*Math.cos(p.tilt/180*Math.PI);
        p.y1=y+p.axis*Math.sin(p.tilt/180*Math.PI);
        p.x2=x+(p.len-p.axis)*Math.cos(p.tilt/180*Math.PI);
        p.y2=y-(p.len-p.axis)*Math.sin(p.tilt/180*Math.PI);
    }
    else{
        p.x1=x+p.axis*Math.cos(p.tilt/180*Math.PI);
        p.y1=y-p.axis*Math.sin(p.tilt/180*Math.PI);
        p.x2=x-(p.len-p.axis)*Math.cos(p.tilt/180*Math.PI);
        p.y2=y+(p.len-p.axis)*Math.sin(p.tilt/180*Math.PI);
    }
    //p.draw();
}



class Pillar {
    constructor(canvas, x1, y1, x2, y2, width, color,lineCap = "round") {
        let ctx = canvas.getContext('2d');
        this.len = Math.sqrt((y2 - y1) * (y2 - y1) + (x2 - x1) * (x2 - x1));
        this.width = width;
        this.tilt = Math.atan((y2 - y1) / (x1 - x2)) / Math.PI * 180;
        this.axis = 0; //this.length/2;
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;
        this.dr = 0;
        this.dx = 0;
        this.dy = 0;
        this.color = color;
        this.draw = function () {
            ctx.beginPath();
            ctx.strokeStyle = this.color;
            ctx.moveTo(this.x1, this.y1);
            ctx.lineTo(this.x2, this.y2);
            ctx.lineWidth = this.width;
            ctx.lineCap =lineCap;
            ctx.stroke();
            ctx.closePath();
        };
        this.draw();
        this.move = function () {
             {
                let h1 = this.y1;
                let h2 = this.y2;
                this.x1 += this.dx;
                this.x2 += this.dx;
                this.y1 += this.dy;
                this.y2 += this.dy;
            }
            this.rota();
        };
        this.rota = function () {
             {
                let x0 = this.x2 * this.axis / this.len + (1 - this.axis / this.len) * this.x1;
                let y0 = this.y2 * this.axis / this.len + (1 - this.axis / this.len) * this.y1;
                let rx1 = Math.cos(this.dr / 10) * (this.x1 - x0) - Math.sin(this.dr / 10) * (this.y1 - y0) + x0;
                let ry1 = Math.sin(this.dr / 10) * (this.x1 - x0) + Math.cos(this.dr / 10) * (this.y1 - y0) + y0;
                let rx2 = Math.cos(this.dr / 10) * (this.x2 - x0) - Math.sin(this.dr / 10) * (this.y2 - y0) + x0;
                let ry2 = Math.sin(this.dr / 10) * (this.x2 - x0) + Math.cos(this.dr / 10) * (this.y2 - y0) + y0;
                this.x1 = rx1;
                this.y1 = ry1;
                this.x2 = rx2;
                this.y2 = ry2;
                this.tilt = Math.atan((this.y2 - this.y1) / (this.x1 - this.x2)) / Math.PI * 180;
            }
            //this.draw();
        }; //*/

    }
}

class Dot {
    constructor(canvas, x, y, r, color) {
        //document.getElementById("p1").innerHTML+="c1";
        let ctx = canvas.getContext('2d');
        this.x = x;
        this.y = y;
        this.r = r;
        this.color = color;
        this.v=2;
        this.target=[x,y];
        //document.getElementById("p1").innerHTML+="c2";
        this.draw = function () {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.r, 0, 2 * Math.PI, false);
            ctx.fillStyle = this.color;
            ctx.fill();
            ctx.closePath();
            //document.getElementById("p1").innerHTML+="c3";
        };//*/
        this.move=function(){
         let d=Math.sqrt(Math.pow((this.x-this.target[0]),2)+Math.pow((this.y-this.target[1]),2));
      if(d>1){
          this.x+=this.v*(this.target[0]-this.x)/d;
          this.y+=this.v*(this.target[1]-this.y)/d;
      }
      this.draw();
       //document.getElementById("p1").innerHTML+="c3";
       };
    }
}

function creatdot(){
    let p=new Dot(canvas,200,200,4,1,0);
    document.getElementById("p1").innerHTML+=p.x;
}

function setDot(dotlist){
    dot.length=0;
    pillar.length=0;
    trace.length=0;	
    if(dot.length){
        dot.length=0;
        pillar.length=0
    }
    else 
        draw();
    for(let i=0;i<dotlist.length;i++){
        dot[dot.length]=new Dot(canvas,dotlist[i][0][0]*ratio,dotlist[i][0][1]*ratio,3,"rgba(0,0,255,1)");
        dot[dot.length]=new Dot(canvas,dotlist[i][1][0]*ratio,dotlist[i][1][1]*ratio,3,"rgba(255,0,0,1)");		
    }
    document.getElementById("P").innerHTML="布点完成";
    document.getElementById("p1").innerHTML="端点数:&nbsp;"+dot.length;
}

function circle(canvas,x,y,r,color,width=0.8){
    let ctx= canvas.getContext('2d');
    ctx.beginPath();
    ctx.arc(x,y,r,0,2*Math.PI,false);
    ctx.strokeStyle=color;
    ctx.lineWidth=width;
    ctx.stroke();
    ctx.closePath();
}

function showCanvas(canvas,dataUrl,offset=11) {
    let ctx= canvas.getContext('2d');
    let img = new Image();
    //console.info(dataUrl);
    img.onload = function () { //加载图片
        let iw = this.width;
        let ih = this.height;
        let local = positionFit(canvas,iw, ih,offset);
        ctx.fillStyle = 'white';
        ctx.fill();
        ctx.drawImage(this, local.px, local.py, local.pw, local.ph);
        if(offset<11) 
            document.getElementById("P").innerHTML="原图尺寸:&nbsp;"+iw+"&times;"+ih;
        //imgData=ctx.getImageData(0,0,cw,ch); 
    }
    img.src =dataUrl;
}

function positionFit(c,pw,ph,offset=0) {
    let devia=0;
    let pad=0;
    let px = 0;
    let py = pad;
    let w=c.width;
    let h=c.height;
    if(Math.min(pw,ph)>Math.max(w,h)){//图片大于canvas
        if(pw<ph){ //长的图,取上部
            devia=(ph/pw*w-h)/2;
            py=0-devia*(1+offset/10);
            ph=h+devia*2;
            pw=w;
            //ph=h+devia*2-pad;    
         }
         else if(pw>ph){ //扁的图,取中部
            devia=(pw*h/ph-w)/2;
            px=0-devia*(1-offset/10);
            pw=w+devia*2;
            ph=h;  
         }
         else{
             pw=w;
             ph=h;
         }
    }
    else{
        if(pw < w && ph < h){
            px = 0.5 * w - 0.5 * pw;
            py = 0.5 * h - 0.5 * ph;
        }
        else if (ph / pw > h / w) {
            let uu = ph;
            ph = h;
            pw = pw * h / uu;
            px = 0.5 * w - 0.5 * pw;
        } 
        else {
            let uu = pw;
            pw = w;
            ph = ph * pw / uu;
            py = 0.5 * h - 0.5 * ph;
        }//*/
    }
    //document.getElementById("p1").innerHTML+="/"+px+"/"+py+"/"+pw+"/"+ph;
    return {px, py, pw, ph};
}