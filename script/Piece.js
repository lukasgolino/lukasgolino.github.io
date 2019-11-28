(function(window) {
	
	var PI2 = Math.PI/2;
	var PI4 = Math.PI/4;
	
	var Piece = function(canvas, config)
	{
		this.initialize(canvas, config);
	}
	var p = Piece.prototype = new BasePiece();
	//
	p.shape;
	//
	p.initialize = function(canvas, config)
	{
		BasePiece.prototype.initialize.apply(this, [canvas, config]);
		this.stage.autoClear = false;
		this.ratios = [0,1];
		this.dangle = this.config.bounceRandomAngle / 180 * Math.PI;
		this.initInteraction();
		document.body.style.backgroundColor = this.config.bgColor;
	}
	
	p.initInteraction = function()
	{
		var that = this;
		//this.stage.addEventListener("stagemousemove", function(e) { that.onMouseMove(e); });
		this.stage.addEventListener("stagemouseup", function(e) { that.onClick(e); });
		//this.stage.addEventListener("dblclick", function(e) { that.onDoubleClick(e); });//dbl click not fired for touch
	}
	
	p.onClick = function(e)
	{
		var t = Date.now();
		if (t-this.lastClick<250)
		{
			this.lastClick = 0;
			this.paused = false;
			this.reset();
		}
		else
		{
			this.lastClick = t;
			//Lukas1
			this.colors = generateRandomColourPair();
			//this.colors = pick(this.config.colorPairs, [this.colors]);
		}
	}
	
	
	p.onKeyUp = function(e)
	{
		BasePiece.prototype.onKeyUp.apply(this, [e]);
		if (!this.config.debug) return;
		var c = String.fromCharCode(e.which);
		if (c=="G") this.generate();
	}
	
	p.setSize = function(w,h,dpr)
	{
		this.dpr = dpr;
		this.width = w*dpr;
		this.height = h*dpr;
		this.diag = Math.sqrt(this.width*this.width+this.height*this.height);
		this.offset = this.diag * this.config.offset;
		this.size = Math.round(this.config.size * Math.min(this.width,this.height));
		//
		var m = Math.min(this.width,this.height) * this.config.margin;
		this.rect = new Rectangle(m,m,this.width-2*m,this.height-2*m);
		if (this.tickLast) this.reset();
	}
	
	p.start = function()
	{
		BasePiece.prototype.start.apply(this);
		this.count = 0;
		this.reset();
	}
	p.reset = function()
	{
		this.stage.clear();
		//this.x = Math.round(this.stage.mouseX ? this.stage.mouseX : Math.random()*(this.width-2*this.size) + this.size);
		//this.y = Math.round(this.stage.mouseY ? this.stage.mouseY : Math.random()*(this.height-2*this.size) + this.size);
		this.x = Math.random()*(this.width-2*this.size) + this.size;
		this.y = Math.random()*(this.height-2*this.size) + this.size;
		this.changeAngle(Math.floor(Math.random()*4) * PI2 + PI4);
		//Lukas
		this.colors = generateRandomColourPair();
		//this.colors = pick(this.config.colorPairs);
	}
	p.changeAngle = function(angle)
	{
		this.count ++;
		var a = PI4 + Math.random()*2*this.dangle-this.dangle;
		a += Math.floor(angle/PI2) * PI2;
		this.setAngle(a);
	}
	p.setAngle = function(angle)
	{
		this.angle = angle;
		this.dx = Math.cos(this.angle) * this.offset;
		this.dy = Math.sin(this.angle) * this.offset;
	}
	
	p.update = function()
	{
		var ctx = this.stage.canvas.getContext("2d");
		ctx.save();
		var vp = this.rect, l = vp.x, r2 = vp.x+vp.width, t = vp.y, b = vp.y+vp.height;
		var r = this.size*.5;
		for (var i=0;i<this.config.circlesPerFrame;i++)
		{
			this.x += this.dx;
			this.y += this.dy;
			//
			if ((this.x-r<l && this.dx<0) || (this.x+r>r2 && this.dx>0))
			{
				this.changeAngle(Math.atan2(this.dy, -this.dx));
			}
			if ((this.y-r<t && this.dy<0) || (this.y+r>b && this.dy>0))
			{
				this.changeAngle(Math.atan2(-this.dy, this.dx));
			}
			this.addCircle(this.x, this.y, r, ctx);
		}
		ctx.restore();
		return false;
	}
		
	p.addCircle = function(x,y,r, ctx)
	{
		var shape = new Shape();
		shape.graphics.lf(this.colors, this.ratios, x-r,y,x+r,y).dc(x,y,r);
		//manually draw only new shape
		shape.updateContext(ctx);
		shape.draw(ctx);
	}
	
	// UTILITY METHODS
	
	var pick = function(pool, exceptions)
	{
		if (exceptions != null)
		{
			var pool2 = [];
			var n = pool.length;
			for (var i = 0; i < n; i++)
			{
				var item = pool[i];
				if (exceptions.indexOf(item) == -1) pool2.push(item);
			}
			pool = pool2;
		}
		return pool[Math.floor(Math.random() * pool.length)];
	}

	var getRandomColor = function() 
	{
		var letters = '0123456789ABCDEF';
		var color = '#';
		for (var i = 0; i < 6; i++) {
		  color += letters[Math.floor(Math.random() * 16)];
		}
		return color;
	  }

	var generateRandomColourPair = function()
	{
		c1 = getRandomColor();
		c2 = getRandomColor();
		pair = [c1, c2];
		return pair;
	}
	
	window.Piece = Piece;
}(window));

