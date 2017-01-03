if renderPixelAspect > 1 then (
	global finalWidth = renderWidth * renderPixelAspect
	global finalHeight = renderHeight
)
else (
	global finalWidth = renderWidth
	global finalHeight = renderHeight / renderPixelAspect
)

fn existDir dname = (getDirectories dname).count != 0
fn formatFrame n =
(
	if n < 10 then
		return "000" + (n as string)
	else if n < 100 then
		return "00" + (n as string)
	else if n < 1000 do
		return "0" + (n as string)
	return n
)

function mkPreviewSeq previewDir fileName sizex sizey startFrame endFrame =
(
	view_size = getViewSize()
	cropH = (view_size.x-sizex)/2
	cropV = (view_size.y-sizey)/2
	for t = startFrame to endFrame do
	(
		sliderTime = t
		
		dib = gw.getViewportDib()
		outputName = previewDir + fileName + formatFrame(t) + ".png"
		anim_bmp = bitmap view_size.x view_size.y
		cropped_bmp = bitmap sizex sizey filename:outputName
		copy dib anim_bmp
		pasteBitmap anim_bmp cropped_bmp (box2 cropH cropV (view_size.x-cropH) (view_size.y-cropV) ) [0,0]
		save cropped_bmp
		close anim_bmp
		close cropped_bmp
	)
)

fn resizeViewport sizeX sizeY = (
	viewSize = getViewSize()
		xRatio = sizeX / viewSize.x
		yRatio = sizeY / viewSize.y
	if xRatio > yRatio then theRatio = xRatio
	else theRatio = yRatio
	convX = viewSize.x * theRatio
	convY = viewSize.y * theRatio
	gw.setPos 0 0 convX convY --setup viewport to desired size
	max views redraw --redraw the view
)

temp = GetDir #preview + "/temp/"
rangeStart = 0
rangeEnd = 10
sizex = finalWidth * 100/100
sizey = finalHeight * 100/100
origLayout = viewport.getLayout()

-- store actual viewport settings
wasMaximized = false
wasFramed = false

-- prepare viewport
if viewport.numviews != 1 then (
	max tool maximize
	wasMaximized = true
)
if not displaySafeFrames then (
	displaySafeFrames = true
	wasFramed = true
)
resizeViewport sizex sizey

mkPreviewSeq temp "frame" sizex sizey rangeStart rangeEnd

-- restore viewport
if wasMaximized then
	max tool maximize
if wasFramed then
	displaySafeFrames = false
