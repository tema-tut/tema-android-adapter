# -*- coding: utf-8
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

"""


"""

import sys
import os
sys.path.append(os.path.realpath(".."))

import re
import time
import gc
from threading import Thread

import unittest
from  AndroidAdapter.guireader import GuiReader
from  AndroidAdapter.monkeydriver import MonkeyDriver 
import guireader_test

from AndroidAdapter.object_keyword import *
from AndroidAdapter.ui_keywords import *


LISTDUMP = """com.android.internal.policy.impl.PhoneWindow$DecorView@43d4c3d8 mForeground=4,null mForegroundInPadding=4,true mForegroundPaddingBottom=1,0 mForegroundPaddingLeft=1,0 mForegroundPaddingRight=1,0 mForegroundPaddingTop=1,0 mMeasureAllChildren=5,false mForegroundGravity=3,119 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=3,480 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,25169208 mID=5,NO_ID mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=3,480 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=3,480 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=4,true isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
 android.widget.LinearLayout@43d4c6d0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=2,25 mMeasuredHeight=3,480 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=3,480 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653314 getBaseline()=2,-1 getHeight()=3,480 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
  android.widget.FrameLayout@43d4ce20 mForeground=4,null mForegroundInPadding=4,true mForegroundPaddingBottom=1,0 mForegroundPaddingLeft=1,0 mForegroundPaddingRight=1,0 mForegroundPaddingTop=1,0 mMeasureAllChildren=5,false mForegroundGravity=3,119 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,2 mPaddingLeft=1,6 mPaddingRight=1,6 mPaddingTop=1,1 mMeasuredHeight=2,25 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,25169200 mID=5,NO_ID mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=2,25 mBottom=2,50 mUserPaddingBottom=1,2 mUserPaddingRight=1,6 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,25 layout_gravity=4,NONE layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=2,25 layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=4,true isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
   android.widget.TextView@43d4d0c0 mText=8,Settings getEllipsize()=3,END mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,308 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,22 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,314 mScrollX=1,0 mScrollY=1,0 mTop=1,1 mBottom=2,23 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,16 getHeight()=2,22 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,308 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
  android.widget.FrameLayout@43d4dcd8 mForeground=52,android.graphics.drawable.NinePatchDrawable@43d4df00 mForegroundInPadding=4,true mForegroundPaddingBottom=1,0 mForegroundPaddingLeft=1,0 mForegroundPaddingRight=1,0 mForegroundPaddingTop=1,0 mMeasureAllChildren=5,false mForegroundGravity=2,55 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=3,430 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=10,id/content mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=2,50 mBottom=3,480 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=3,430 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=1,0 layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
   android.widget.ListView@43d4e028 recycleOnMeasure()=4,true getSelectedView()=36,android.widget.LinearLayout@43d36b20 isFastScrollEnabled()=5,false isScrollingCacheEnabled()=4,true isSmoothScrollbarEnabled()=4,true isStackFromBottom()=5,false isTextFilterEnabled()=5,false mNextSelectedPosition=1,0 mSelectedPosition=1,0 mItemCount=2,14 mFirstPosition=1,0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=5,false isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=3,430 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,18352178 mID=7,id/list mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=3,430 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402940417 getBaseline()=2,-1 getHeight()=3,430 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=4,true isFocused()=4,true isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.LinearLayout@43d36b20 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=2,64 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=2,10 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780468 mID=15,id/widget_frame mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,64 mUserPaddingBottom=1,0 mUserPaddingRight=2,10 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,64 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=4,true isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.ImageView@43ddfd10 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,32 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,32 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780340 mID=7,id/icon mRight=2,38 mScrollX=1,0 mScrollY=1,0 mTop=2,16 mBottom=2,48 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,32 layout_gravity=6,CENTER layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,32 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=4,true isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.RelativeLayout@43d346d8 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,258 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=2,46 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780468 mID=5,NO_ID mRight=3,304 mScrollX=1,0 mScrollY=1,0 mTop=2,17 mBottom=2,47 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,30 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,6 layout_leftMargin=1,2 layout_rightMargin=1,6 layout_topMargin=1,6 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,258 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=4,true isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.widget.TextView@43df4ab8 mText=19,Wireless & networks getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,202 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779316 mID=8,id/title mRight=3,202 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,202 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=4,true isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      android.widget.TextView@43d03c40 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=1,0 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=1,0 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16781316 mID=10,id/summary mRight=1,0 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653192 getBaseline()=2,-1 getHeight()=1,0 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=8,id/title layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=4,true isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.LinearLayout@43da2430 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=2,64 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=2,10 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=15,id/widget_frame mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=2,65 mBottom=3,129 mUserPaddingBottom=1,0 mUserPaddingRight=2,10 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,64 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.ImageView@43dd2340 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,32 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,32 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=7,id/icon mRight=2,38 mScrollX=1,0 mScrollY=1,0 mTop=2,16 mBottom=2,48 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,32 layout_gravity=6,CENTER layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,32 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.RelativeLayout@43d4f108 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,258 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=2,46 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,304 mScrollX=1,0 mScrollY=1,0 mTop=2,17 mBottom=2,47 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,30 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,6 layout_leftMargin=1,2 layout_rightMargin=1,6 layout_topMargin=1,6 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,258 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.widget.TextView@43da2c60 mText=13,Call settings getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,119 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,119 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,119 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      android.widget.TextView@43dcdbd0 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=1,0 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=1,0 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16781312 mID=10,id/summary mRight=1,0 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653192 getBaseline()=2,-1 getHeight()=1,0 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=8,id/title layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.LinearLayout@43d492c0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=2,64 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=2,10 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=15,id/widget_frame mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=3,130 mBottom=3,194 mUserPaddingBottom=1,0 mUserPaddingRight=2,10 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,64 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.ImageView@43d4a7f0 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,32 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,32 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=7,id/icon mRight=2,38 mScrollX=1,0 mScrollY=1,0 mTop=2,16 mBottom=2,48 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,32 layout_gravity=6,CENTER layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,32 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.RelativeLayout@43d4f4f0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,258 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=2,46 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,304 mScrollX=1,0 mScrollY=1,0 mTop=2,17 mBottom=2,47 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,30 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,6 layout_leftMargin=1,2 layout_rightMargin=1,6 layout_topMargin=1,6 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,258 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.widget.TextView@43ddf0e8 mText=15,Sound & display getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,161 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,161 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,161 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      android.widget.TextView@43dca928 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=1,0 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=1,0 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16781312 mID=10,id/summary mRight=1,0 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653192 getBaseline()=2,-1 getHeight()=1,0 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=8,id/title layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.LinearLayout@43d2a8c0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=2,64 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=2,10 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=15,id/widget_frame mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=3,195 mBottom=3,259 mUserPaddingBottom=1,0 mUserPaddingRight=2,10 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,64 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.ImageView@43d2aae0 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,32 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,32 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=7,id/icon mRight=2,38 mScrollX=1,0 mScrollY=1,0 mTop=2,16 mBottom=2,48 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,32 layout_gravity=6,CENTER layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,32 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.RelativeLayout@43ddf548 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,258 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=2,46 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,304 mScrollX=1,0 mScrollY=1,0 mTop=2,17 mBottom=2,47 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,30 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,6 layout_leftMargin=1,2 layout_rightMargin=1,6 layout_topMargin=1,6 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,258 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.widget.TextView@43de1830 mText=19,Location & security getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,190 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,190 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,190 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      android.widget.TextView@43d83578 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=1,0 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=1,0 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16781312 mID=10,id/summary mRight=1,0 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653192 getBaseline()=2,-1 getHeight()=1,0 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=8,id/title layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.LinearLayout@43da9290 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=2,64 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=2,10 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=15,id/widget_frame mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=3,260 mBottom=3,324 mUserPaddingBottom=1,0 mUserPaddingRight=2,10 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,64 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.ImageView@43dab108 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,32 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,32 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=7,id/icon mRight=2,38 mScrollX=1,0 mScrollY=1,0 mTop=2,16 mBottom=2,48 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,32 layout_gravity=6,CENTER layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,32 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.RelativeLayout@43dab588 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,258 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=2,46 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,304 mScrollX=1,0 mScrollY=1,0 mTop=2,17 mBottom=2,47 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,30 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,6 layout_leftMargin=1,2 layout_rightMargin=1,6 layout_topMargin=1,6 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,258 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.widget.TextView@43da1d98 mText=12,Applications getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,122 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,122 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,122 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      android.widget.TextView@43de1d68 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=1,0 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=1,0 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16781312 mID=10,id/summary mRight=1,0 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653192 getBaseline()=2,-1 getHeight()=1,0 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=8,id/title layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.LinearLayout@43d85838 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=2,64 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=2,10 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=15,id/widget_frame mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=3,325 mBottom=3,389 mUserPaddingBottom=1,0 mUserPaddingRight=2,10 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,64 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.ImageView@43d9bef8 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,32 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,32 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=7,id/icon mRight=2,38 mScrollX=1,0 mScrollY=1,0 mTop=2,16 mBottom=2,48 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,32 layout_gravity=6,CENTER layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,32 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.RelativeLayout@43da8928 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,258 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=2,46 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,304 mScrollX=1,0 mScrollY=1,0 mTop=2,17 mBottom=2,47 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,30 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,6 layout_leftMargin=1,2 layout_rightMargin=1,6 layout_topMargin=1,6 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,258 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.widget.TextView@43d28818 mText=15,Accounts & sync getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,160 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,160 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,160 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      android.widget.TextView@43d51e38 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=1,0 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=1,0 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16781312 mID=10,id/summary mRight=1,0 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653192 getBaseline()=2,-1 getHeight()=1,0 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=8,id/title layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.LinearLayout@43d7cbc8 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=2,64 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=2,10 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=15,id/widget_frame mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=3,390 mBottom=3,454 mUserPaddingBottom=1,0 mUserPaddingRight=2,10 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,64 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.ImageView@43d847e8 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,32 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,32 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=7,id/icon mRight=2,38 mScrollX=1,0 mScrollY=1,0 mTop=2,16 mBottom=2,48 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,32 layout_gravity=6,CENTER layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,32 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.RelativeLayout@43d84bc8 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,258 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=2,46 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,304 mScrollX=1,0 mScrollY=1,0 mTop=2,17 mBottom=2,47 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,30 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,6 layout_leftMargin=1,2 layout_rightMargin=1,6 layout_topMargin=1,6 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,258 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.widget.TextView@43d82920 mText=7,Privacy getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,69 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=2,69 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,69 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      android.widget.TextView@43d47e68 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=1,0 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=1,0 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16781312 mID=10,id/summary mRight=1,0 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653192 getBaseline()=2,-1 getHeight()=1,0 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=8,id/title layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
DONE.

"""

LISTDUMP2 = """com.android.internal.policy.impl.PhoneWindow$DecorView@43d4c3d8 mForeground=4,null mForegroundInPadding=4,true mForegroundPaddingBottom=1,0 mForegroundPaddingLeft=1,0 mForegroundPaddingRight=1,0 mForegroundPaddingTop=1,0 mMeasureAllChildren=5,false mForegroundGravity=3,119 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=3,480 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,25169208 mID=5,NO_ID mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=3,480 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=3,480 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=4,true isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
 android.widget.LinearLayout@43d4c6d0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=2,25 mMeasuredHeight=3,480 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=3,480 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653314 getBaseline()=2,-1 getHeight()=3,480 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
  android.widget.FrameLayout@43d4ce20 mForeground=4,null mForegroundInPadding=4,true mForegroundPaddingBottom=1,0 mForegroundPaddingLeft=1,0 mForegroundPaddingRight=1,0 mForegroundPaddingTop=1,0 mMeasureAllChildren=5,false mForegroundGravity=3,119 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,2 mPaddingLeft=1,6 mPaddingRight=1,6 mPaddingTop=1,1 mMeasuredHeight=2,25 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,25169200 mID=5,NO_ID mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=2,25 mBottom=2,50 mUserPaddingBottom=1,2 mUserPaddingRight=1,6 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,25 layout_gravity=4,NONE layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=2,25 layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=4,true isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
   android.widget.TextView@43d4d0c0 mText=8,Settings getEllipsize()=3,END mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,308 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,22 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,314 mScrollX=1,0 mScrollY=1,0 mTop=1,1 mBottom=2,23 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,16 getHeight()=2,22 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,308 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
  android.widget.FrameLayout@43d4dcd8 mForeground=52,android.graphics.drawable.NinePatchDrawable@43d4df00 mForegroundInPadding=4,true mForegroundPaddingBottom=1,0 mForegroundPaddingLeft=1,0 mForegroundPaddingRight=1,0 mForegroundPaddingTop=1,0 mMeasureAllChildren=5,false mForegroundGravity=2,55 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=3,430 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=10,id/content mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=2,50 mBottom=3,480 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=3,430 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=1,0 layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
   android.widget.ListView@43d4e028 recycleOnMeasure()=4,true getSelectedView()=36,android.widget.LinearLayout@43d0a888 isFastScrollEnabled()=5,false isScrollingCacheEnabled()=4,true isSmoothScrollbarEnabled()=4,true isStackFromBottom()=5,false isTextFilterEnabled()=5,false mNextSelectedPosition=2,13 mSelectedPosition=2,13 mItemCount=2,14 mFirstPosition=1,7 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=5,false isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=3,430 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,18352178 mID=7,id/list mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=3,430 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402940417 getBaseline()=2,-1 getHeight()=3,430 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=4,true isFocused()=4,true isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.LinearLayout@43dd63a0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=2,64 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=2,10 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16812208 mID=15,id/widget_frame mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=3,-24 mBottom=2,40 mUserPaddingBottom=1,0 mUserPaddingRight=2,10 mViewFlags=9,402686080 getBaseline()=2,-1 getHeight()=2,64 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=4,true isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.ImageView@43dd9630 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,32 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,32 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=7,id/icon mRight=2,38 mScrollX=1,0 mScrollY=1,0 mTop=2,16 mBottom=2,48 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,32 layout_gravity=6,CENTER layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,32 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.RelativeLayout@43dd3e10 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,258 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=2,46 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779440 mID=5,NO_ID mRight=3,304 mScrollX=1,0 mScrollY=1,0 mTop=2,17 mBottom=2,47 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,30 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,6 layout_leftMargin=1,2 layout_rightMargin=1,6 layout_topMargin=1,6 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,258 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.widget.TextView@43d2a158 mText=23,SD card & phone storage getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,247 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,247 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,247 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      android.widget.TextView@43d31ec8 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=1,0 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=1,0 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16781312 mID=10,id/summary mRight=1,0 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653192 getBaseline()=2,-1 getHeight()=1,0 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=8,id/title layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.LinearLayout@43d797f0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=2,64 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=2,10 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=15,id/widget_frame mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=2,41 mBottom=3,105 mUserPaddingBottom=1,0 mUserPaddingRight=2,10 mViewFlags=9,402686080 getBaseline()=2,-1 getHeight()=2,64 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=4,true isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.ImageView@43ddee28 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,32 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,32 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=7,id/icon mRight=2,38 mScrollX=1,0 mScrollY=1,0 mTop=2,16 mBottom=2,48 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,32 layout_gravity=6,CENTER layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,32 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.RelativeLayout@43d361a0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,258 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=2,46 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,304 mScrollX=1,0 mScrollY=1,0 mTop=2,17 mBottom=2,47 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,30 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,6 layout_leftMargin=1,2 layout_rightMargin=1,6 layout_topMargin=1,6 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,258 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.widget.TextView@43d862e0 mText=6,Search getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,66 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=2,66 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,66 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      android.widget.TextView@43d87c50 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=1,0 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=1,0 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16781312 mID=10,id/summary mRight=1,0 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653192 getBaseline()=2,-1 getHeight()=1,0 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=8,id/title layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.LinearLayout@43d923d0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=2,64 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=2,10 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=15,id/widget_frame mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=3,106 mBottom=3,170 mUserPaddingBottom=1,0 mUserPaddingRight=2,10 mViewFlags=9,402686080 getBaseline()=2,-1 getHeight()=2,64 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=4,true isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.ImageView@43d92848 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,32 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,32 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=7,id/icon mRight=2,38 mScrollX=1,0 mScrollY=1,0 mTop=2,16 mBottom=2,48 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,32 layout_gravity=6,CENTER layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,32 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.RelativeLayout@43d92cc0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,258 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=2,46 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,304 mScrollX=1,0 mScrollY=1,0 mTop=2,17 mBottom=2,47 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,30 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,6 layout_leftMargin=1,2 layout_rightMargin=1,6 layout_topMargin=1,6 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,258 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.widget.TextView@43d881e0 mText=19,Language & keyboard getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,216 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,216 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,216 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      android.widget.TextView@43d5fba0 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=1,0 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=1,0 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16781312 mID=10,id/summary mRight=1,0 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653192 getBaseline()=2,-1 getHeight()=1,0 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=8,id/title layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.LinearLayout@43dc1fa0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=2,64 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=2,10 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=15,id/widget_frame mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=3,171 mBottom=3,235 mUserPaddingBottom=1,0 mUserPaddingRight=2,10 mViewFlags=9,402686080 getBaseline()=2,-1 getHeight()=2,64 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=4,true isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.ImageView@43dc29f8 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,32 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,32 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=7,id/icon mRight=2,38 mScrollX=1,0 mScrollY=1,0 mTop=2,16 mBottom=2,48 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,32 layout_gravity=6,CENTER layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,32 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.RelativeLayout@43dd4568 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,258 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=2,46 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,304 mScrollX=1,0 mScrollY=1,0 mTop=2,17 mBottom=2,47 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,30 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,6 layout_leftMargin=1,2 layout_rightMargin=1,6 layout_topMargin=1,6 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,258 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.widget.TextView@43d86878 mText=13,Accessibility getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,120 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,120 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,120 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      android.widget.TextView@43d875b8 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=1,0 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=1,0 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16781312 mID=10,id/summary mRight=1,0 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653192 getBaseline()=2,-1 getHeight()=1,0 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=8,id/title layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.LinearLayout@43d343a0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=2,64 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=2,10 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=15,id/widget_frame mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=3,236 mBottom=3,300 mUserPaddingBottom=1,0 mUserPaddingRight=2,10 mViewFlags=9,402686080 getBaseline()=2,-1 getHeight()=2,64 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=4,true isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.ImageView@43d353e0 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,32 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,32 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=7,id/icon mRight=2,38 mScrollX=1,0 mScrollY=1,0 mTop=2,16 mBottom=2,48 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,32 layout_gravity=6,CENTER layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,32 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.RelativeLayout@43d35a90 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,258 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=2,46 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,304 mScrollX=1,0 mScrollY=1,0 mTop=2,17 mBottom=2,47 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,30 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,6 layout_leftMargin=1,2 layout_rightMargin=1,6 layout_topMargin=1,6 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,258 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.widget.TextView@43d8b848 mText=14,Text-to-speech getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,145 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,145 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,145 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      android.widget.TextView@43dceb90 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=1,0 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=1,0 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16781312 mID=10,id/summary mRight=1,0 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653192 getBaseline()=2,-1 getHeight()=1,0 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=8,id/title layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.LinearLayout@43dcfda0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=2,64 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=2,10 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=15,id/widget_frame mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=3,301 mBottom=3,365 mUserPaddingBottom=1,0 mUserPaddingRight=2,10 mViewFlags=9,402686080 getBaseline()=2,-1 getHeight()=2,64 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=4,true isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.ImageView@43dd0c78 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,32 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,32 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780336 mID=7,id/icon mRight=2,38 mScrollX=1,0 mScrollY=1,0 mTop=2,16 mBottom=2,48 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,32 layout_gravity=6,CENTER layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,32 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.RelativeLayout@43dd3478 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,258 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=2,46 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,304 mScrollX=1,0 mScrollY=1,0 mTop=2,17 mBottom=2,47 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,30 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,6 layout_leftMargin=1,2 layout_rightMargin=1,6 layout_topMargin=1,6 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,258 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.widget.TextView@43df59e8 mText=11,Date & time getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,117 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,117 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,117 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      android.widget.TextView@43d3b2d8 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=1,0 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=1,0 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16781312 mID=10,id/summary mRight=1,0 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653192 getBaseline()=2,-1 getHeight()=1,0 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=8,id/title layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.LinearLayout@43d0a888 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=2,64 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=2,10 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780468 mID=15,id/widget_frame mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=3,366 mBottom=3,430 mUserPaddingBottom=1,0 mUserPaddingRight=2,10 mViewFlags=9,402686080 getBaseline()=2,-1 getHeight()=2,64 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=4,true isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=4,true isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
     android.widget.ImageView@43dd6e70 mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,32 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,32 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780340 mID=7,id/icon mRight=2,38 mScrollX=1,0 mScrollY=1,0 mTop=2,16 mBottom=2,48 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653184 getBaseline()=2,-1 getHeight()=2,32 layout_gravity=6,CENTER layout_weight=3,0.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,32 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=4,true isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
     android.widget.RelativeLayout@43d27058 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,258 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=2,46 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780468 mID=5,NO_ID mRight=3,304 mScrollX=1,0 mScrollY=1,0 mTop=2,17 mBottom=2,47 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,30 layout_gravity=4,NONE layout_weight=3,1.0 layout_bottomMargin=1,6 layout_leftMargin=1,2 layout_rightMargin=1,6 layout_topMargin=1,6 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,258 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=4,true isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
      android.widget.TextView@43dcb198 mText=11,About phone getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,129 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779316 mID=8,id/title mRight=3,129 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402657280 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,129 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=4,true isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
      android.widget.TextView@43df7b10 mText=0, getEllipsize()=4,null mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=1,0 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=1,0 mLeft=1,0 mPrivateFlags_FORCE_LAYOUT=6,0x1000 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_NOT_DRAWN=3,0x0 mPrivateFlags=8,16781316 mID=10,id/summary mRight=1,0 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=1,0 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653192 getBaseline()=2,-1 getHeight()=1,0 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=8,id/title layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=11,false/NO_ID layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=4,GONE getWidth()=1,0 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=5,false isOpaque()=5,false isSelected()=4,true isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
DONE.

"""

MENUDUMP = """com.android.internal.policy.impl.PhoneWindow$DecorView@43d6a4d8 mForeground=4,null mForegroundInPadding=4,true mForegroundPaddingBottom=1,0 mForegroundPaddingLeft=1,0 mForegroundPaddingRight=1,0 mForegroundPaddingTop=1,0 mMeasureAllChildren=5,false mForegroundGravity=3,119 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=1,2 mPaddingRight=1,2 mPaddingTop=2,12 mMeasuredHeight=3,143 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780592 mID=5,NO_ID mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=3,143 mUserPaddingBottom=1,0 mUserPaddingRight=1,2 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=3,143 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
 com.android.internal.view.menu.IconMenuView@43d6aab0 getDescendantFocusability()=23,FOCUS_AFTER_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,316 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=3,131 mLeft=1,2 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780338 mID=12,id/icon_menu mRight=3,318 mScrollX=1,0 mScrollY=1,0 mTop=2,12 mBottom=3,143 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402915329 getBaseline()=2,-1 getHeight()=3,131 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,316 hasFocus()=4,true isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=4,true isFocused()=4,true isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
  com.android.internal.view.menu.IconMenuItemView@43d78aa0 mText=10,New window getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,104 mPaddingBottom=1,1 mPaddingLeft=1,1 mPaddingRight=1,1 mPaddingTop=1,1 mMeasuredHeight=2,65 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,104 mScrollX=4,8141 mScrollY=1,4 mTop=1,0 mBottom=2,65 mUserPaddingBottom=1,1 mUserPaddingRight=1,1 mViewFlags=9,402673665 getBaseline()=2,64 getHeight()=2,65 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,104 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
  com.android.internal.view.menu.IconMenuItemView@43e29138 mText=9,Bookmarks getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,104 mPaddingBottom=1,1 mPaddingLeft=1,1 mPaddingRight=1,1 mPaddingTop=1,1 mMeasuredHeight=2,65 mLeft=3,105 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,210 mScrollX=4,8141 mScrollY=1,4 mTop=1,0 mBottom=2,65 mUserPaddingBottom=1,1 mUserPaddingRight=1,1 mViewFlags=9,402673665 getBaseline()=2,64 getHeight()=2,65 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,105 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
  com.android.internal.view.menu.IconMenuItemView@43d3ab78 mText=7,Windows getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,104 mPaddingBottom=1,1 mPaddingLeft=1,1 mPaddingRight=1,1 mPaddingTop=1,1 mMeasuredHeight=2,65 mLeft=3,211 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,316 mScrollX=4,8141 mScrollY=1,4 mTop=1,0 mBottom=2,65 mUserPaddingBottom=1,1 mUserPaddingRight=1,1 mViewFlags=9,402673665 getBaseline()=2,64 getHeight()=2,65 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,105 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
  com.android.internal.view.menu.IconMenuItemView@43dddbc0 mText=7,Refresh getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,104 mPaddingBottom=1,1 mPaddingLeft=1,1 mPaddingRight=1,1 mPaddingTop=1,1 mMeasuredHeight=2,65 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,104 mScrollX=4,8141 mScrollY=1,4 mTop=2,66 mBottom=3,131 mUserPaddingBottom=1,1 mUserPaddingRight=1,1 mViewFlags=9,402673665 getBaseline()=2,64 getHeight()=2,65 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,104 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
  com.android.internal.view.menu.IconMenuItemView@43d62db0 mText=7,Forward getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,104 mPaddingBottom=1,1 mPaddingLeft=1,1 mPaddingRight=1,1 mPaddingTop=1,1 mMeasuredHeight=2,65 mLeft=3,105 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,210 mScrollX=4,8141 mScrollY=1,4 mTop=2,66 mBottom=3,131 mUserPaddingBottom=1,1 mUserPaddingRight=1,1 mViewFlags=9,402673697 getBaseline()=2,64 getHeight()=2,65 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,105 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=5,false isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
  com.android.internal.view.menu.IconMenuItemView@43e29d08 mText=4,More getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,104 mPaddingBottom=1,1 mPaddingLeft=1,1 mPaddingRight=1,1 mPaddingTop=1,1 mMeasuredHeight=2,65 mLeft=3,211 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,316 mScrollX=4,8141 mScrollY=1,4 mTop=2,66 mBottom=3,131 mUserPaddingBottom=1,1 mUserPaddingRight=1,1 mViewFlags=9,402673665 getBaseline()=2,64 getHeight()=2,65 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=11,FILL_PARENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,105 hasFocus()=5,false isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
DONE.

"""

MOREMENUDUMP = """com.android.internal.policy.impl.PhoneWindow$DecorView@43d6a4d8 mForeground=4,null mForegroundInPadding=4,true mForegroundPaddingBottom=1,0 mForegroundPaddingLeft=1,0 mForegroundPaddingRight=1,0 mForegroundPaddingTop=1,0 mMeasureAllChildren=5,false mForegroundGravity=3,119 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,320 mPaddingBottom=1,0 mPaddingLeft=2,12 mPaddingRight=2,12 mPaddingTop=2,12 mMeasuredHeight=3,455 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780592 mID=5,NO_ID mRight=3,320 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=3,455 mUserPaddingBottom=1,0 mUserPaddingRight=2,12 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=3,455 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,320 hasFocus()=4,true isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
 com.android.internal.view.menu.ExpandedMenuView@43d21188 recycleOnMeasure()=5,false getSelectedView()=4,null isFastScrollEnabled()=5,false isScrollingCacheEnabled()=4,true isSmoothScrollbarEnabled()=4,true isStackFromBottom()=5,false isTextFilterEnabled()=5,false mNextSelectedPosition=2,-1 mSelectedPosition=2,-1 mItemCount=1,7 mFirstPosition=1,0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=5,false isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,296 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=3,443 mLeft=2,12 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,18352178 mID=16,id/expanded_menu mRight=3,308 mScrollX=1,0 mScrollY=1,0 mTop=2,12 mBottom=3,455 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402940417 getBaseline()=2,-1 getHeight()=3,443 layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=3,296 getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,296 hasFocus()=4,true isClickable()=4,true isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=4,true isFocusableInTouchMode()=4,true isFocused()=4,true isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
  com.android.internal.view.menu.ListMenuItemView@43d3c9a0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,294 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,1 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,295 mScrollX=1,0 mScrollY=1,0 mTop=1,1 mBottom=2,65 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,64 layout_height=2,64 layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,294 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
   android.widget.RelativeLayout@43dd6240 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,282 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,49 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,288 mScrollX=1,0 mScrollY=1,0 mTop=1,7 mBottom=2,56 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,406847616 getBaseline()=2,-1 getHeight()=2,49 layout_gravity=15,CENTER_VERTICAL layout_weight=3,1.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=1,0 getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,282 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
    android.widget.TextView@43dadad8 mText=12,Add bookmark getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,282 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,282 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,406851584 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=4,true layout_mRules_alignParentTop=4,true layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,282 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.TextView@43e19c70 mText=6,Menu+a getEllipsize()=3,END mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,51 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,19 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=11,id/shortcut mRight=2,51 mScrollX=1,0 mScrollY=1,0 mTop=2,30 mBottom=2,49 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,406847488 getBaseline()=2,15 getHeight()=2,19 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=4,true layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,51 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
  com.android.internal.view.menu.ListMenuItemView@43d471d0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,294 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,64 mLeft=1,1 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,295 mScrollX=1,0 mScrollY=1,0 mTop=2,66 mBottom=3,130 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,402653312 getBaseline()=2,-1 getHeight()=2,64 layout_height=2,64 layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,294 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
   android.widget.RelativeLayout@43dd66c0 getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS getPersistentDrawingCache()=9,SCROLLING isAlwaysDrawnWithCacheEnabled()=4,true isAnimationCacheEnabled()=4,true isChildrenDrawingOrderEnabled()=5,false isChildrenDrawnWithCacheEnabled()=5,false mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,282 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,49 mLeft=1,6 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16780464 mID=5,NO_ID mRight=3,288 mScrollX=1,0 mScrollY=1,0 mTop=1,7 mBottom=2,56 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,406847616 getBaseline()=2,-1 getHeight()=2,49 layout_gravity=15,CENTER_VERTICAL layout_weight=3,1.0 layout_bottomMargin=1,0 layout_leftMargin=1,6 layout_rightMargin=1,6 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=1,0 getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,282 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=4,true 
    android.widget.TextView@43dde988 mText=12,Find on page getEllipsize()=7,MARQUEE mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=3,282 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,30 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=8,id/title mRight=3,282 mScrollX=1,0 mScrollY=1,0 mTop=1,0 mBottom=2,30 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,406851584 getBaseline()=2,24 getHeight()=2,30 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=11,false/NO_ID layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=4,true layout_mRules_alignParentTop=4,true layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=11,FILL_PARENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=3,282 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
    android.widget.TextView@43e11640 mText=6,Menu+f getEllipsize()=3,END mMinWidth=1,0 mMinHeight=1,0 mMeasuredWidth=2,49 mPaddingBottom=1,0 mPaddingLeft=1,0 mPaddingRight=1,0 mPaddingTop=1,0 mMeasuredHeight=2,19 mLeft=1,0 mPrivateFlags_DRAWING_CACHE_INVALID=3,0x0 mPrivateFlags_DRAWN=4,0x20 mPrivateFlags=8,16779312 mID=11,id/shortcut mRight=2,49 mScrollX=1,0 mScrollY=1,0 mTop=2,30 mBottom=2,49 mUserPaddingBottom=1,0 mUserPaddingRight=1,0 mViewFlags=9,406847488 getBaseline()=2,15 getHeight()=2,19 layout_mRules_leftOf=11,false/NO_ID layout_mRules_rightOf=11,false/NO_ID layout_mRules_above=11,false/NO_ID layout_mRules_below=8,id/title layout_mRules_alignBaseline=11,false/NO_ID layout_mRules_alignLeft=11,false/NO_ID layout_mRules_alignTop=11,false/NO_ID layout_mRules_alignRight=11,false/NO_ID layout_mRules_alignBottom=11,false/NO_ID layout_mRules_alignParentLeft=4,true layout_mRules_alignParentTop=11,false/NO_ID layout_mRules_alignParentRight=11,false/NO_ID layout_mRules_alignParentBottom=11,false/NO_ID layout_mRules_center=11,false/NO_ID layout_mRules_centerHorizontal=11,false/NO_ID layout_mRules_centerVertical=11,false/NO_ID layout_bottomMargin=1,0 layout_leftMargin=1,0 layout_rightMargin=1,0 layout_topMargin=1,0 layout_height=12,WRAP_CONTENT layout_width=12,WRAP_CONTENT getTag()=4,null getVisibility()=7,VISIBLE getWidth()=2,49 hasFocus()=5,false isClickable()=5,false isDrawingCacheEnabled()=5,false isEnabled()=4,true isFocusable()=5,false isFocusableInTouchMode()=5,false isFocused()=5,false isHapticFeedbackEnabled()=4,true isInTouchMode()=4,true isOpaque()=5,false isSelected()=5,false isSoundEffectsEnabled()=4,true willNotCacheDrawing()=5,false willNotDraw()=5,false 
DONE.

"""

class MockTarget():

	def __init__(self,name,monkey_port, window_port):
		self.__name = name
		self.__monkey_port = monkey_port
		self.__window_port = window_port
		
		self.__monkeydriver = MockMonkey()
		self.__guireader = MockReader(self.__name, self.__monkeydriver, port = self.__window_port)


	def setup(self):

		self.__monkeydriver = MockMonkey()
		self.__guireader = MockReader(self.__name, self.__monkeydriver, port = self.__window_port)
		
		return True	

	def getName(self):
		return self.__name

	def getGUIReader(self):
		return self.__guireader

	def getMonkeyDriver(self):
		return self.__monkeydriver


class MockReader(GuiReader):
    
    def __init__(self, target, monkey, host ="g", port = 2):
        GuiReader.__init__(self,target,monkey,host,port)
        self.__dump = guireader_test.dumpdataok2.splitlines()
    
    def readGUI(self):    
        self.__processScreenDump__(self.__dump)

    def setScreenDump(self, dump):  
        self.__dump = dump.splitlines()
    
    def __getForegroundWindowCoordinates__(self):           
        return 0,0
       
class MockMonkey(MonkeyDriver):

    def __init__(self):
        self.mockreader = None
        self.listtest = False
        self.menutest = False
        self.wasscrolled = False
        MonkeyDriver.__init__(self)
        self.taptimes = 0
        self.lastcommand = ""

    def setGuiReader(self,mockreader):
        self.mockreader = mockreader

    def wasScrolled(self):
        return self.wasscrolled

    def getTapTimes(self):
        return self.taptimes
        
    def getLastCommand(self):
        return self.lastcommand

    def startListTest(self):
        self.listtest = True
        self.mockreader.setScreenDump(LISTDUMP)
        
    def startMenuTest(self):
        self.menutest = True
        self.mockreader.setScreenDump(MENUDUMP)

    def getScreenSize(self):
        return 320,480
        
    def getPlatformVersion(self):
        return "2.1"	
        
    def __sendCommand__(self,command):

        self.lastcommand = command.strip()
        if command.startswith("tap"):
            self.taptimes += 1
        return True	
        
    def sendPress(self, key):

        if key == "DPAD_DOWN" and self.listtest:
            self.mockreader.setScreenDump(LISTDUMP2)
            self.wasscrolled = True
            
        return self.__sendCommand__("press " + key)

    def sendTap(self,x,y):
        
        if self.menutest:
            self.mockreader.setScreenDump(MOREMENUDUMP)

        return self.__sendCommand__("tap " + str(x) + " " + str(y))

    
class TestKeyword(unittest.TestCase):
    """
    Keyword superclass tests
    """
    
    def setUp(self):
        self.__keyword = Keyword()
    
    
    #----------Pattern tests----------#   
       
    def testPatternValid(self):
        self.__keyword.attributePattern = re.compile("kw_something(param)?")
        self.assert_(self.__keyword.isMyKeyword("kw_something")) 
        
    def testPatternInvalid(self):
        self.__keyword.attributePattern = re.compile("kw_something")
        self.assertFalse(self.__keyword.isMyKeyword("kw_error")) 
    



class TestObjectKeyword(unittest.TestCase):


    def setUp(self):
        self.__keyword = ObjectKeyword()
        self.__keyword.initialize("",MockTarget("emulator-5554",1,1))


    #----------MatchComponent tests----------#
     
    def testMatchComponentFull(self):

        compName = "parent1:::'parent2'::comp"
        compRole = "role;Name"
        name, role = self.__keyword.matchComponent(compName + ";" + compRole)
        print name,role
        self.assert_(compName == name and compRole == role)
        
    def testMatchComponentNoRole(self):

        compName = "parent1:::parent2::comp"
        name, role = self.__keyword.matchComponent(compName)
        self.assert_(compName == name and role == None) 
    
    def testMatchComponentNoName(self):

        compRole = "roleName"
        name, role = self.__keyword.matchComponent(";" + compRole)
        self.assert_(name == "" and compRole == role)
    
    def testMatchComponentEmpty(self):

        name, role = self.__keyword.matchComponent("")
        self.assert_(name == "" and role == None)
    
    def testMatchComponentNone(self):

        name, role = self.__keyword.matchComponent(None)
        self.assert_(name == None and role == None)
   


    #----------findComponent tests----------#   
 
    #Basic references
    def testFindComponentBasic(self):

        component = "id/digit5"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node != None and node.getId() == "id/digit5")
        
    def testFindComponentBasic2(self):

        component = "id/digit5;com.android.calculator2.ColorButton"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node != None and node.getId() == "id/digit5" and node.getClassName() == "com.android.calculator2.ColorButton")
    
    def testFindComponentAll(self):

        component = "'7'"
        node = self.__keyword.findComponentReference(component, True)
        self.assert_(node != None and isinstance(node,list) and len(node) == 2)
   
    def testFindComponentAllNotFound(self):

        component = "safd asfksadfb lksabglkjsag lkjsaglkjsadf"
        node = self.__keyword.findComponentReference(component, True)
        self.assert_(node == None)   
    
    
    #Hierarchical references
    
    def testFindComponentHierarchicalRefFound(self):

        component = "root::id/content::::id/display;CalculatorDisplay"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node != None and node.getId() == "id/display" and node.getParent().getParent().getId() == "id/content" and node.getClassName() == "com.android.calculator2.CalculatorDisplay")  
        
    def testFindComponentHierarchicalComplicated(self):

        component = "root::::::id/display;CalculatorDisplay"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node != None and node.getId() == "id/display" and node.getParent().getParent().getId() == "id/content" and node.getClassName() == "com.android.calculator2.CalculatorDisplay")  
     
    def testFindComponentHierarchicalRefNotFound(self):

        component = "root::nonono::nonothing;nothing"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node == None)        

    def testFindComponentHierarchicalRefNotFound2(self):

        component = "root::id/content::id/display;LinearNONO"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node == None)   
    
    #Descendant references
    
    def testFindComponentDescendant(self):

        component = "root:::id/digit5;com.android.calculator2.ColorButton"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node != None and node.getId() == "id/digit5" and node.getClassName() == "com.android.calculator2.ColorButton")
        
    def testFindComponentDescendant2(self):

        component = "root:::id/content:::id/digit5"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node != None and node.getId() == "id/digit5" and node.getParent().getClassName() == "android.widget.ListView")       
    
    def testFindComponentDescendantNotFound(self):

        component = "root:::id/digit5;asdasd"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node == None)                 
    
    def testFindComponentDescendantNotFound2(self):

        component = "root:::ei pittaas olla taman nimmiista"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node == None) 
    

    #mixed references
    
    def testFindComponentMixed(self):

        component = "root::id/content:::id/digit5;ColorButton"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node != None and node.getId() == "id/digit5") 
 
    def testFindComponentMixedAtLeastOneGeneration(self):

        component = "root:::::id/digit5;ColorButton"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node != None and node.getId() == "id/digit5")     
    
    #reference contains text content
   
    def testFindComponentByTextContent(self):

        component = "'5';ColorButton"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node != None and node.getId() == 'id/digit5') 
    
    def testFindComponentByTextContent2(self):

        component = "root:::id/content:::'6';ColorButton"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node != None and node.getId() == 'id/digit6')
    
    def testFindComponentByTextContent3(self):

        component = "root::id/content:::'6';ColorButton"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node != None and node.getId() == 'id/digit6')
    
    def testFindComponentByTextContent4(self):

        component = "root::id/content:::::::::'6';ColorButton"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node != None and node.getId() == 'id/digit6')
    
    
    def testFindComponentByTextContentNotFound(self):

        component = "root::id/content::::::::::::'3'::'4';menu"
        node = self.__keyword.findComponentReference(component)
        self.assert_(node == None) 
 

    

#----------------------------------------------------------------------------#


    #----------VerifyText tests----------#
class TestKeywordVerifyText(unittest.TestCase):


    def setUp(self):
        self.__keyword = VerifyText()
        
  
    def testVerifyTextPattern(self):
        
        self.assert_(self.__keyword.isMyKeyword("'6'"))

        self.assert_(self.__keyword.isMyKeyword("'texthere',root"))
        
        self.assertFalse(self.__keyword.isMyKeyword("textwithoutapostrophes,root"))
                
        
    def testVerifySuccess(self):

        self.__keyword.initialize("'5',id/digit5",MockTarget("emulator-5554",1,1))
        self.assert_(self.__keyword.execute())
                     
    def testVerifySuccess2(self):
    
        self.__keyword.initialize("'5',root",MockTarget("emulator-5554",1,1))
        self.assert_(self.__keyword.execute())
        
    def testVerifyFails(self):

        self.__keyword.initialize("'5', id/content:::id/digit6;ColorButton",MockTarget("emulator-5554",1,1))
        self.assertFalse(self.__keyword.execute())
        
    def testVerifyFails2(self):

        self.__keyword.initialize("'THIS TEXT IS NOT FOUND FROM THE SCREEN'",MockTarget("emulator-5554",1,1))
        self.assertFalse(self.__keyword.execute())


    #----------WaitText tests----------#  
class TestKeywordWaitText(unittest.TestCase):


    def setUp(self):
    
        self.__keyword = WaitText()
    
    def testWaitTextPattern(self):
    
        self.assert_(self.__keyword.isMyKeyword("'texthere',,"))

        self.assert_(self.__keyword.isMyKeyword("'texthere',10,root"))
        
        self.assertFalse(self.__keyword.isMyKeyword("textwithoutapostrophes,root"))
       
    def testWaitTextSuccessImmediately(self):

        self.__keyword.initialize("'5',root",MockTarget("emulator-5554",1,1))        
        self.assert_(self.__keyword.execute())
        
    def testWaitTextSuccessLater(self):
    
        class Threader(Thread):
        
            def __init__(self,mockreader):
                self.__mockreader = mockreader
                Thread.__init__(self)    
            
            def run(self):
                time.sleep(1)
                self.__mockreader.setScreenDump(guireader_test.dumpdataok2)
                
           
        mocktarget = MockTarget("emulator-5554",1,1)
        self.__keyword.initialize("'5',5,root",mocktarget)  
        mocktarget.getGUIReader().setScreenDump(guireader_test.dumpdataok)
        
        threader = Threader(mocktarget.getGUIReader())
        threader.start()
        
        self.assert_(self.__keyword.execute())

    
    def testWaitTextFail(self):
    
        self.__keyword.initialize("'notfoundohdear',1,root",MockTarget("emulator-5554",1,1))
        self.assertFalse(self.__keyword.execute()) 
        
        
    #----------WaitObject tests----------#  
class TestKeywordWaitObject(unittest.TestCase):


    def setUp(self):
    
        self.__keyword = WaitObject()
    
    def testWaitObjectPattern(self):
    
        self.assert_(self.__keyword.isMyKeyword("'textcomponent'"))

        self.assert_(self.__keyword.isMyKeyword("10,root"))
        
    def testWaitObjectSuccessImmediately(self):

        self.__keyword.initialize("id/digit5",MockTarget("emulator-5554",1,1))        
        self.assert_(self.__keyword.execute())

    def testWaitObjectSuccessImmediately2(self):

        self.__keyword.initialize("'5'",MockTarget("emulator-5554",1,1))        
        self.assert_(self.__keyword.execute())
        
    def testWaitObjectSuccessLater(self):
    
        class Threader(Thread):
        
            def __init__(self,mockreader):
                self.__mockreader = mockreader
                Thread.__init__(self)    
            
            def run(self):
                time.sleep(1)
                self.__mockreader.setScreenDump(guireader_test.dumpdataok2)
                
        
        mocktarget = MockTarget("emulator-5554",1,1)
        self.__keyword.initialize("5,id/digit5",mocktarget)     
 
        mocktarget.getGUIReader().setScreenDump(guireader_test.dumpdataok)
        
        threader = Threader(mocktarget.getGUIReader())
        threader.start()
        
        self.assert_(self.__keyword.execute())

    
    def testWaitObjectFail(self):
    
        self.__keyword.initialize("2,notfoundohdear",MockTarget("emulator-5554",1,1))
        self.assertFalse(self.__keyword.execute()) 
        
        
    #----------SelectFromList tests----------#  
class TestKeywordSelectFromList(unittest.TestCase):

    def setUp(self):
    
        self.__keyword = SelectFromList()
        self.__mocktarget = MockTarget("emulator-5554",1,1)
        self.__mockmonkey = self.__mocktarget.getMonkeyDriver()
        self.__mockreader = self.__mocktarget.getGUIReader()
        self.__mockmonkey.setGuiReader(self.__mockreader)
        self.__mockmonkey.startListTest()
           
    
    def testSelectFromListPattern(self):
    
        self.assert_(self.__keyword.isMyKeyword("'listItem'"))

        self.assert_(self.__keyword.isMyKeyword("'listitem',true"))

        self.assert_(self.__keyword.isMyKeyword("'listitem',false"))

        self.assertFalse(self.__keyword.isMyKeyword("noapostrophes"))    
   
    def testSelectFromListSuccessImmediately(self):
       
        self.__keyword.initialize("'Applications'",self.__mocktarget)        
        self.assert_(self.__keyword.execute())
        self.assertFalse(self.__mockmonkey.wasScrolled())

    def testSelectFromListSuccessAfterScroll(self):

        self.__keyword.initialize("'Accessibility'",self.__mocktarget)        
        self.assert_(self.__keyword.execute())
        self.assert_(self.__mockmonkey.wasScrolled())    

    
    def testSelectFromListFail(self):
    
        self.__keyword.initialize("'notfoundohdear'",self.__mocktarget)
        self.assertFalse(self.__keyword.execute()) 
        self.assert_(self.__mockmonkey.wasScrolled())


    #----------TapCoordinate tests----------#  
class TestKeywordTapCoordinate(unittest.TestCase):

    def setUp(self):
    
        self.__keyword = TapCoordinate()
        self.__mocktarget = MockTarget("emulator-5554",1,1)
        self.__mockmonkey = self.__mocktarget.getMonkeyDriver()
        self.__mockreader = self.__mocktarget.getGUIReader()
        self.__mockmonkey.setGuiReader(self.__mockreader)
        

    def testTapCoordinatePattern(self):
    
        self.assert_(self.__keyword.isMyKeyword("111,111"))
      
        self.assert_(self.__keyword.isMyKeyword("500,500"))

        self.assertFalse(self.__keyword.isMyKeyword("a,b"))    

        self.assertFalse(self.__keyword.isMyKeyword("-12,-123"))    
   
    def testTapCoordinateSuccess(self):
       
        self.__keyword.initialize("10,10",self.__mocktarget)        
        self.assert_(self.__keyword.execute())
    
    def testTapCoordinateFail(self):
    
        self.__keyword.initialize("3000,3000",self.__mocktarget)
        self.assertFalse(self.__keyword.execute()) 
    
    #TODO: tests for other coordinate based tapping keywords
  

    #----------TapObject tests----------#  
class TestKeywordTapObject(unittest.TestCase):

    def setUp(self):
    
        self.__keyword = TapObject()
        self.__mocktarget = MockTarget("emulator-5554",1,1)
        self.__mockmonkey = self.__mocktarget.getMonkeyDriver()
        self.__mockreader = self.__mocktarget.getGUIReader()

        

    def testTapObjectPattern(self):
    
        self.assert_(self.__keyword.isMyKeyword("'object'"))

        self.assert_(self.__keyword.isMyKeyword("object"))

        self.assert_(self.__keyword.isMyKeyword("2,id/digit5"))
   
    def testTapObjectSuccess(self):
       
        self.__keyword.initialize("3,id/digit5",self.__mocktarget)        
        self.assert_(self.__keyword.execute())
        self.assert_(self.__mockmonkey.getTapTimes() == 3)
        self.assert_(self.__mockmonkey.getLastCommand() == "tap 120 285")
    
    def testTapObjectFail(self):
    
        self.__keyword.initialize("notexists",self.__mocktarget)
        self.assertFalse(self.__keyword.execute()) 


    #----------TapObject tests----------#  
class TestKeywordDrag(unittest.TestCase):

    def setUp(self):
    
        self.__keyword = Drag()
        self.__mocktarget = MockTarget("emulator-5554",1,1)
        self.__mockmonkey = self.__mocktarget.getMonkeyDriver()
        self.__mockreader = self.__mocktarget.getGUIReader()   

    def testDragPattern(self):
    
        self.assert_(self.__keyword.isMyKeyword("100,100 --> 200,200"))

        self.assert_(self.__keyword.isMyKeyword("object --> object2"))

        self.assert_(self.__keyword.isMyKeyword("100,200 --> 'a'"))

        self.assert_(self.__keyword.isMyKeyword("'a' --> 200,50"))

   
    def testDragSuccess(self):
       
        self.__keyword.initialize("200,300 --> 300,400",self.__mocktarget)        
        self.assert_(self.__keyword.execute())
        self.assert_(self.__mockmonkey.getLastCommand() == "touch up 300 400")
      
  
    def testDragSuccess2(self):
       
        self.__keyword.initialize("id/digit4-->id/digit5",self.__mocktarget)        
        self.assert_(self.__keyword.execute())
        self.assert_(self.__mockmonkey.getLastCommand() == "touch up 120 285")
      
    
    def testDragFail(self):
    
        self.__keyword.initialize("notexists --> 400",self.__mocktarget)
        self.assertFalse(self.__keyword.execute()) 


    #----------SelectFromMenu tests----------#  
class TestKeywordSelectFromMenu(unittest.TestCase):

    def setUp(self):
    
        self.__keyword = SelectFromMenu()
        self.__mocktarget = MockTarget("emulator-5554",1,1)
        self.__mockmonkey = self.__mocktarget.getMonkeyDriver()
        self.__mockreader = self.__mocktarget.getGUIReader()
        self.__mockmonkey.setGuiReader(self.__mockreader)

    def testSelectFromMenuPattern(self):
              
        self.assert_(self.__keyword.isMyKeyword("'menuitem'"))
        self.assertFalse(self.__keyword.isMyKeyword("noapostrophes"))

    def testSelectFromMenuSuccessImmediately(self):
    
        self.__keyword.initialize("'Refresh'",self.__mocktarget)    
        self.__mockmonkey.startMenuTest()
        self.assert_(self.__keyword.execute())
        self.assert_(self.__mockmonkey.getLastCommand() == "tap 54 110")

    def testSelectFromMenuMore(self):
    
        self.__keyword.initialize("'Add bookmark'",self.__mocktarget)    
        self.__mockmonkey.startMenuTest()
        self.assert_(self.__keyword.execute())
        self.assert_(self.__mockmonkey.getLastCommand() == "tap 160 35")       


#----------CheckProperty tests----------#  
class TestKeywordCheckProperty(unittest.TestCase):

	def setUp(self):

		self.__keyword = CheckProperty()
		self.__mocktarget = MockTarget("emulator-5554",1,1)
		self.__mockmonkey = self.__mocktarget.getMonkeyDriver()
		self.__mockreader = self.__mocktarget.getGUIReader()    

	def testCheckPropertyPattern(self):
			  
		self.assert_(self.__keyword.isMyKeyword("propname,'value',object"))
		self.assert_(self.__keyword.isMyKeyword("propname,'value','objectwithtext'"))

		self.assertFalse(self.__keyword.isMyKeyword("a,'b'"))
		self.assertFalse(self.__keyword.isMyKeyword("a,b,c"))


	def testCheckPropertySuccess(self):

		self.__keyword.initialize("isInTouchMode(),'true',id/digit8",self.__mocktarget)    
		self.assert_(self.__keyword.execute())

	def testCheckPropertyFail(self):

		self.__keyword.initialize("isInTouchMode(), 'false', id/digit8",self.__mocktarget)    
		self.assertFalse(self.__keyword.execute())
	
	def testCheckPropertyFailNotFound(self):

		self.__keyword.initialize("isInTouchModesss(), 'true', id/digit8",self.__mocktarget)    
		self.assertFalse(self.__keyword.execute())

	def testCheckPropertyFailNotFound2(self):

		self.__keyword.initialize("isInTouchMode(), 'false', id/digiasd",self.__mocktarget)    
		self.assertFalse(self.__keyword.execute())


#----------LaunchApp tests----------#  
class TestKeywordLaunchApp(unittest.TestCase):

	def setUp(self):

		self.__keyword = LaunchApp()
		self.__mocktarget = MockTarget("emulator-5554",1,1)
		self.__mockmonkey = self.__mocktarget.getMonkeyDriver()
		self.__mockreader = self.__mocktarget.getGUIReader()     

	def testLaunchAppPattern(self):
			  
		self.assert_(self.__keyword.isMyKeyword("'application'"))
		self.assert_(self.__keyword.isMyKeyword("'recent:application'"))
		self.assert_(self.__keyword.isMyKeyword("'appmenu:application'"))
		self.assert_(self.__keyword.isMyKeyword("'aaa.bbb.cc::ddd.eee'"))
		
		self.assertFalse(self.__keyword.isMyKeyword("a"))

"""
	def testLaunchAppSuccess(self):

		self.__keyword.initialize("isInTouchMode(),'true',id/digit8",self.__mockmonkey,self.__mockreader)    
		self.assert_(self.__keyword.execute())

	def testLaunchAppFail(self):

		self.__keyword.initialize("isInTouchMode(), 'false', id/digit8",self.__mockmonkey,self.__mockreader)    
		self.assertFalse(self.__keyword.execute())
	
	def testLaunchAppFailNotFound(self):

		self.__keyword.initialize("isInTouchModesss(), 'true', id/digit8",self.__mockmonkey,self.__mockreader)    
		self.assertFalse(self.__keyword.execute())

	def testLaunchAppFailNotFound2(self):

		self.__keyword.initialize("isInTouchMode(), 'false', id/digiasd",self.__mockmonkey,self.__mockreader)    
		self.assertFalse(self.__keyword.execute())

"""          
   
         
#----------------------------------MAIN--------------------------------------#

if __name__ == '__main__':


    baseKw = unittest.TestLoader().loadTestsFromTestCase(TestKeyword)
    objectKw = unittest.TestLoader().loadTestsFromTestCase(TestObjectKeyword) 
    verify = unittest.TestLoader().loadTestsFromTestCase(TestKeywordVerifyText)
    waitText = unittest.TestLoader().loadTestsFromTestCase(TestKeywordWaitText)
    waitObject = unittest.TestLoader().loadTestsFromTestCase(TestKeywordWaitObject)
    selectfromlist = unittest.TestLoader().loadTestsFromTestCase(TestKeywordSelectFromList)
    tapcoortest = unittest.TestLoader().loadTestsFromTestCase(TestKeywordTapCoordinate)
    tapobj = unittest.TestLoader().loadTestsFromTestCase(TestKeywordTapObject)
    drag = unittest.TestLoader().loadTestsFromTestCase(TestKeywordDrag)
    menu = unittest.TestLoader().loadTestsFromTestCase(TestKeywordSelectFromMenu)
    checkprop = unittest.TestLoader().loadTestsFromTestCase(TestKeywordCheckProperty)
    launchapp = unittest.TestLoader().loadTestsFromTestCase(TestKeywordLaunchApp)
    

    #typeTests = unittest.TestLoader().loadTestsFromTestCase(TestKeywordType)
    #isTrue = unittest.TestLoader().loadTestsFromTestCase(TestKeywordIsTrue)
    #searchRoot = unittest.TestLoader().loadTestsFromTestCase(TestKeywordSetSearchRoot)
    #click = unittest.TestLoader().loadTestsFromTestCase(TestKeywordClickComponent)
    #press = unittest.TestLoader().loadTestsFromTestCase(TestKeywordPressComponent)
    #release = unittest.TestLoader().loadTestsFromTestCase(TestKeywordReleaseComponent)
    
    kwTests = unittest.TestSuite([verify, waitText, waitObject, selectfromlist, tapcoortest, tapobj,drag,menu,checkprop,launchapp])
    
    allTests = unittest.TestSuite([baseKw,objectKw,kwTests])
    unittest.TextTestRunner(verbosity=2).run(allTests)


