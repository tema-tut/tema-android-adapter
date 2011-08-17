#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2006-2010 Tampere University of Technology
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys
import os
sys.path.append(os.path.realpath(".."))

from AndroidAdapter import guireader
import socket
from threading import Thread
import unittest


# verdicts:

PASS,FAIL="PASS","FAIL"


dumpdataok = """com.android.internal.policy.impl.PhoneWindow$DecorView@43d06398 mForeground=4,null 
 android.widget.FrameLayout@43d06690 mForeground=52,android.graphics.drawable.NinePatchDrawable@43d2c3e8 mForegroundInPadding=5,false 
DONE.

"""

dumpdataok2 = """com.android.internal.policy.impl.PhoneWindow$DecorView@43d06398 mForeground=4,null mForegroundInPadding=4,true mForegroundPaddingBottom=1,0 mForegroundPaddingLeft=1,0 mForegroundPaddingRight=1,0 mForegroundPaddingTop=1,0 mMeasureAllChildren=5,false mForegroundGravity=3,119 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=3,480 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,25169208 mID=5,NO_ID mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=3,480 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=3,480 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=4,true isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
 android.widget.FrameLayout@43d06690 mForeground=52,android.graphics.drawable.NinePatchDrawable@43d2c3e8 mForegroundInPadding=5,false mForegroundPaddingBottom=1,0 mForegroundPaddingLeft=1,0 mForegroundPaddingRight=1,0 mForegroundPaddingTop=1,0 mMeasureAllChildren=5,false mForegroundGravity=2,55 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=2,25 mMeasuredHeight=3,480 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=10,id/content mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=3,480 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653186 getBaseline()=2,-1 getHeight()=3,480 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
  android.widget.LinearLayout@43d2c4e0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=3,455 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,25169200 mID=5,NO_ID mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=2,25 mBottom=3,480 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=3,455 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=4,true isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
   com.android.calculator2.CalculatorDisplay@43d2c730 mForeground=4,null mForegroundInPadding=4,true mForegroundPaddingBottom=1,0 mForegroundPaddingLeft=1,0 mForegroundPaddingRight=1,0 mForegroundPaddingTop=1,0 mMeasureAllChildren=4,true mForegroundGravity=3,119 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,91 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=10,id/display mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,91 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,61 getHeight()=2,91 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=1,0 layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
    android.widget.EditText@43d2c9b8 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,8 mPaddingLeft=1,8 mPaddingRight=1,8 mPaddingTop=1,8 mMeasuredHeight=2,91 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_LAYOUT_REQUIRED=6,0x2000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16792576 mID=5,NO_ID mRight=1,0 mScrollX=5,16396 mScrollY=2,65 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,8 mUserPaddingRight=1,8 mViewFlags=9,405028873 getBaseline()=2,61 getHeight()=1,0 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=4,true isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.EditText@43d07468 mText=1,7 getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,8 mPaddingLeft=1,8 mPaddingRight=1,8 mPaddingTop=1,8 mMeasuredHeight=2,91 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779314 mID=5,NO_ID mRight=3,320 mScrollX=5,16080 mScrollY=1,0 mTop=1,0 mBottom=2,91 mUserPaddingBottom=1,8 mUserPaddingRight=1,8 mViewFlags=9,405028865 getBaseline()=2,61 getHeight()=2,91 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=4,true isFocused()=4,true isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
   com.android.calculator2.PanelSwitcher@43d07f78 mForeground=4,null mForegroundInPadding=4,true mForegroundPaddingBottom=1,0 mForegroundPaddingLeft=1,0 mForegroundPaddingRight=1,0 mForegroundPaddingTop=1,0 mMeasureAllChildren=5,false mForegroundGravity=3,119 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=3,364 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=14,id/panelswitch mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=2,91 mBottom=3,455 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=3,364 layout_gravity=4,NONE layout_weight=3,4.0 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=1,0 layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
    android.widget.LinearLayout@43d08280 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=3,364 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=12,id/simplePad mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=3,364 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=3,364 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.LinearLayout@43d3a958 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,52 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,52 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,52 layout_gravity=4,NONE layout_weight=3,2.0 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=1,0 layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.view.View@43d3aa98 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,239 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,52 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=5,NO_ID mRight=3,239 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,52 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,52 layout_gravity=4,NONE layout_weight=3,3.0 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=1,0 getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,239 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      com.android.calculator2.ColorButton@43d3ac28 mText=5,CLEAR getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,80 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,52 mLeft=3,240 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=6,id/del mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,52 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,404766721 getBaseline()=2,31 getHeight()=2,52 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,0 layout_leftMargin=1,1 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=1,0 getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,80 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.LinearLayout@43d3b160 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,78 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=2,52 mBottom=3,130 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,78 layout_gravity=4,NONE layout_weight=3,3.0 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=1,0 layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      com.android.calculator2.ColorButton@43d3b370 mText=1,7 getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,79 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,78 mLeft=1,1 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=9,id/digit7 mRight=2,80 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,78 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402669569 getBaseline()=2,54 getHeight()=2,78 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,0 layout_leftMargin=1,1 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,79 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      com.android.calculator2.ColorButton@43d3b8a8 mText=1,8 getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,79 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,78 mLeft=2,81 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=9,id/digit8 mRight=3,160 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,78 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402669569 getBaseline()=2,54 getHeight()=2,78 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,0 layout_leftMargin=1,1 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,79 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      com.android.calculator2.ColorButton@43d3bde0 mText=1,9 getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,79 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,78 mLeft=3,161 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=9,id/digit9 mRight=3,240 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,78 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402669569 getBaseline()=2,54 getHeight()=2,78 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,0 layout_leftMargin=1,1 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,79 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      com.android.calculator2.ColorButton@43d3c318 mText=1,÷ getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,79 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,78 mLeft=3,241 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=6,id/div mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,78 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402669569 getBaseline()=2,54 getHeight()=2,78 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,0 layout_leftMargin=1,1 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,79 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.ListView@43d3c850 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,78 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=3,130 mBottom=3,208 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,78 layout_gravity=4,NONE layout_weight=3,3.0 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=1,0 layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      com.android.calculator2.ColorButton@43d3ca60 mText=1,4 getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,79 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,78 mLeft=1,1 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=9,id/digit4 mRight=2,80 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,78 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402669569 getBaseline()=2,54 getHeight()=2,78 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,0 layout_leftMargin=1,1 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,79 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      com.android.calculator2.ColorButton@43d5fac0 mText=1,5 getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,79 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,78 mLeft=2,81 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=9,id/digit5 mRight=3,160 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,78 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402669569 getBaseline()=2,54 getHeight()=2,78 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,0 layout_leftMargin=1,1 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,79 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      com.android.calculator2.ColorButton@43d5fff8 mText=1,6 getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,79 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,78 mLeft=3,161 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=9,id/digit6 mRight=3,240 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,78 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402669569 getBaseline()=2,54 getHeight()=2,78 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,0 layout_leftMargin=1,1 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,79 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      com.android.calculator2.ColorButton@43d60530 mText=1,× getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,79 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,78 mLeft=3,241 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=6,id/mul mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,78 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402669569 getBaseline()=2,54 getHeight()=2,78 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,0 layout_leftMargin=1,1 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,79 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
DONE.

"""


dumpdataerr = """ERRERRERR"""

dumpdataerr2 = """DONE.
"""


def check_dump_items(items):

    i = items[12]
    if i.getClassName() == "com.android.calculator2.ColorButton" and \
        i.getCode() == "43d3b370" and \
        i.getIndent() == 6 and \
        i.getProperties()["mText"] == "7" and \
        i.getParent().getCode() == "43d3b160" and \
        len(i.getChildren()) == 0:
            return True
    return False

        
class MockDump(Thread):

	def __init__(self):
		self.__dump = ""
		Thread.__init__(self)
	
	def setDump(self,dump):
		self.__dump = dump
	
	
	def close(self):
		self.run = False
		try:
			self.sock.close()
			self.conn.close()
		except:
			pass
	
	def run(self):
		self.run = True
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(("localhost", 4941))
		self.sock.settimeout(2)
		self.sock.listen(1)
		while self.run:
			try:
				self.sock.settimeout(2)
				self.conn, addr = self.sock.accept()
				self.sock.settimeout(0)
				data = self.conn.recv(1024)
				if data.strip() == "DUMP -1":
					for part in self.__dump.splitlines():
						self.conn.sendall(part + "\n")
			except:
				pass
			
			finally:
				try:
					self.conn.close()
				except:
					pass
				
		self.sock.close()
			
class MockMonkey(Thread):
	
	def getScreenSize(self):
		return 320,480
	

class TestGuiReader(unittest.TestCase):

	MOCKD = None
		

	def setUp(self):
		self.__guir = guireader.GuiReader("emulator-5554",MockMonkey(),port = 4941)

	
	def check_dump_items(items):

		i = items[12]
		if i.getClassName() == "com.android.calculator2.ColorButton" and \
			i.getCode() == "43d3b370" and \
			i.getIndent() == 6 and \
			i.getProperties()["mText"] == "7" and \
			i.getParent().getCode() == "43d3b160" and \
			len(i.getChildren()) == 0:
				return True
		return False


	### UNIT TESTs for guireader
	

	def testReadValidGuiDump(self):
		
		TestGuiReader.MOCKD.setDump(dumpdataok)
		self.assert_(self.__guir.readGUI())	
	
	def testReadInvalidGuiDump(self):
	
		TestGuiReader.MOCKD.setDump(dumpdataerr)
		self.assertFalse(self.__guir.readGUI())

	def testReadInvalidGuiDump2(self):
	
		TestGuiReader.MOCKD.setDump(dumpdataerr2)
		self.assertFalse(self.__guir.readGUI())	

	def testProcessValidGuiDump(self):

		items = self.__guir.__processScreenDump__(dumpdataok2.splitlines())
		self.assert_(items != None and len(items) == 21 and check_dump_items(items))

	def testProcessInvalidScreenDump(self):
	
		items = self.__guir.__processScreenDump__(["ERRERRERR"])
		self.assert_(items == None)

	def testProcessScreenDumpInvalidPropertyLength(self):
	
		items = self.__guir.__processScreenDump__(["com.android.calculator2.ColorButton@43d60530 mText=2,×y","com.android.calculator2.ColorButton@43d60530 mText=2,×"])
		self.assert_(items == None)
	
	def testListViewSearch(self):
	
		items = self.__guir.__processScreenDump__(dumpdataok2.splitlines())
		self.assert_(items and self.__guir.getListView().getCode() == "43d3c850")

	def testListViewSearchNoExist(self):
	
		items = self.__guir.__processScreenDump__(dumpdataok.splitlines())
		self.assert_(items and self.__guir.getListView() == None)		
		
	def testComponentSearch(self):
		
		items = self.__guir.__processScreenDump__(dumpdataok2.splitlines())
		item = self.__guir.findComponent(lambda x: x.getCode() == "43d3ac28")
		self.assert_(item and item.getProperties()["mText"] == "CLEAR")

	def testComponentSearchNotExists(self):
		
		items = self.__guir.__processScreenDump__(dumpdataok2.splitlines())
		item = self.__guir.findComponent(lambda x: x.getCode() == "adf")
		self.assert_(item == None)

	def testComponentSearchMultipleComponents(self):
	
		items = self.__guir.__processScreenDump__(dumpdataok2.splitlines())
		items = self.__guir.findComponent(lambda x: x.getClassName() == "com.android.calculator2.ColorButton",searchAll = True)
		self.assert_(len(items) == 9)

	def testComponentSearchWithRoot(self):
	
		items = self.__guir.__processScreenDump__(dumpdataok2.splitlines())
		root = items[0]
		item = self.__guir.findComponent(lambda x: x.getCode() == "43d3ac28", rootItem = root)
		self.assert_(item and item.getProperties()["mText"] == "CLEAR")
		
	def testComponentSearchWithText(self):
	
		items = self.__guir.__processScreenDump__(dumpdataok2.splitlines())
		item = self.__guir.findComponentWithText("CLEAR")
		self.assert_(item and item.getCode() == "43d3ac28")

	def testComponentSearchWithId(self):
	
		items = self.__guir.__processScreenDump__(dumpdataok2.splitlines())
		item = self.__guir.findComponentWithId("id/del")
		self.assert_(item and item.getCode() == "43d3ac28")
"""
	def testGetViewCoordinates(self):
	
		items = self.__guir.__processScreenDump__(dumpdataok2.splitlines())
		item = self.__guir.findComponentWithId("id/digit5")
		x,y = self.__guir.getViewCoordinates(item)
		self.assert_(x == 120 and y == 285)


	def testGetViewCoordinatesPartialyOutOfScreenBottom(self):
	
		items = self.__guir.__processScreenDump__(dumpdataok.splitlines())
		self.assert_(items != None)
		item = self.__guir.findComponentWithId("id/bottom")
		x,y = self.__guir.getViewCoordinates(item)
		print x,y
		#self.assert_(x == 120 and y == 285)
	
	def testGetViewCoordinatesPartiallyOutOfScreenTop(self):
	
		items = self.__guir.__processScreenDump__(dumpdataok.splitlines())
		self.assert_(items != None)
		item = self.__guir.findComponentWithId("id/outtop")
		x,y = self.__guir.getViewCoordinates(item)
		print x,y
		#self.assert_(x == 120 and y == 285)
"""
if __name__ == '__main__':
	
	m = MockDump()
	m.start()
	
	TestGuiReader.MOCKD = m

	tests = unittest.TestLoader().loadTestsFromTestCase(TestGuiReader)
	unittest.TextTestRunner(verbosity=2).run(tests)

	m.close()


