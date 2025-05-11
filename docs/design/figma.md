# Figma

## Color Scheme
The chosen color scheme for the app design closely mirrors the colors used on Hipper’s website. This decision was made after discussions with the team, ensuring the app feels like an authentic extension of the Hipper brand. By aligning the app with the website’s color choices, we aimed to create a seamless and legitimate experience that reinforces Hipper's identity.

![Color Scheme](../assets/Figma/ColorScheme.png)

- The background color: White
- Font color: Black
- The color of the shadow around the boxes: Light blue (color code: 3981C1)

### Dark mode
- Background color: dark grey (color code: 2B2B2B)
- Font color: White (color code: FFFFFF)
- the color of the shadow around the boxes: Light blue (color code: 3981C1)

**References**
- The app used for getting the color code from the website is a macOS app: Digital Color Meter.
- Chatgpt was used to figure out how to use the shadows in figma.

## Navigation Bar
The navbar that is used in the figma design is made into a component, so the it will be reuseable on every page where it is needed. 

### Elements on the navigation bar:

These are to elements used on the navbar:

- The Hipper logo (left-side)
- Shortcuts to Homepage and Profilepage
- Button to log out.

![NavBar](../assets/Figma/NavBar.png)

### Steps to make the component:

1. First you have to design the navbar the way you want it to be.

2. Then you need to group all the elements used in the navbar.

3. After this you can right-click the frame and choose create component or Cmd/Ctrl + Alt + K can be used as a shortcut. Now it will be a reuseable component.

### References
- Chatgpt was used to figure out how to make the reuseable component.

## Visual feedback (Hover effect)
To ensure that users testing the Figma prototype are aware of their actions, we have decided to implement a hover effect. When interacting with buttons or elements in the navbar, the user will see a color change upon hovering, providing clear feedback that the element is being used.

![Normal page](../assets/Figma/ColorScheme.png)

**Above is an image of the normal look of the page.**

![Hover page](../assets/Figma/HoverEffect.png)

**Above is an image of the look of the page with the hover effect.**

### Steps to make the hover effect:

1. Create Two States:

- **Normal State:** Design the button or element as it normally looks.
- **Hover State:** Duplicate the normal state and change the color (or add effects like shadow) for when it's hovered over.

2. Set The Hover Interaction:

- Select the **Normal State**.
- Go to the Prototype tab and drag the blue arrow to the **Hover State**.
- Set the trigger to "While Hovering" and the action to "Smart Animate".

3. Preview The Hover Effect:

- Click Present (top-right) to see the effect in action. When you hover, the element should change color.

4. Add Click Interaction:

- If you want the button to navigate, select the **Normal State**, drag the blue arrow to the target frame, and set the trigger to "On Click".

### References
- Chatgpt is used to help figure out the process of making the hover effect for buttons and the navigation bar.
- Also some youtube video's were used to help with understanding how the make the hover effect. (These will be linked below.)

This video is watched at speed 0.25:  [Navigation Hover Effect in one minute using Figma](https://www.youtube.com/watch?v=CnJIfQRur28)

Video on how to create hover effect on button: [Create a Button With a HOVER Functionality in 128 SECONDS (Figma Tutorial)](https://www.youtube.com/watch?v=AHBEpMD2dZ0)

## Dark mode
To switch to dark mode, there is a button under the profile page where settings can be changed. One of these settings is a button to switch between dark and regular themes. 
