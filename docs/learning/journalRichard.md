# Learning Journal
This file contains the learning journal with the learning story's of Richard.

## Learning Story 105
As a student, I want to learn how to easily get color codes from colors used on websites, so I can easily replicate them if i need to.

### What I have learned.
Before I started working on the design of the app that will be made there was decided that the app will have the same color theme as the official Hipper website, but to do this I needed the find out the color codes of the colors that are used on the website. To get the color code I spoke with a team member and downloaded an app on my macbook. this app could get the color codes, but there was difficulties with getting it to the website to get the color code, so this app didn't work the way I wanted it to work. After searching for a bit for another app. I found out that there was an build in macOS app on my macbook to get the color codes. After working with this app I found the color codes of the colors used on the official Hipper website and started working on the design.

### References
- First app used is named: Color Picker
- Second app used is named: Digital Color Meter

## Learning Story 108
As a student, I want to learn how to make a hover effect on buttons and the navbar in figma, so when using this prototype it will give a more realistic feeling.

### What I have learned.
To make the prototype in figma more realistic I wanted to learn how to make the hover effect for button and the navbar in figma. To make this happen I first asked chatgpt for instructions on how to do this. This helped a bit, but some things were still unclear without seeing it done, so after asking chatgpt and knowing a bit about it I started searching for video's on youtube. The first one I found was about how to make a hover effect on a button. With this video I was finally able to make the hover effect on the button. The second video I watched was also about the hover effect, but this one was about the navbar. At last after watching these video's I was finally able to get it done.

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

Link to figma: [This is the link to figma](https://www.figma.com/design/uE1Wi3VC106f8T5ExqMtoD/School-Projects?node-id=598-2&p=f&t=kHiMl6c36qMbgXLQ-0)

## Learning Story 186
As a student I want to learn how to work with constraints on figma, so I can make the design responsive.

### What I have learned.
To make the pages on figma responsive, so user can also see you visual of the app when using another device I have to learn how to work with constraints. Contraints control how the elements behave when the frame or screen they are in is resized. This is essential for making a responsive design. To learn how to do this I started learning it using youtube video's and asking some simple questions on chatgpt. After gaining some insights on how to work with constraints I started working with them on the homepage of the design in figma. After working on in for some time I finally got some on the elements to be responsive when resizing the page. The only problem was the images of the graphs on the page. I wanted them to be under eachother when resizing, but no matter what I did I couldn't get it to work. After working with the constraints I learned how to use it on the elements to make them responsive. I think the problem with the graphs was to positioning of them in the normal design. I will look into that further when I will be working on the design again. 

![Responsive1](../assets/Figma/ResponsiveDesign1.png)
![Responsive1](../assets/Figma/ResponsiveDesign2.png)

### Steps for work with constraints.

1. Select a Frame as Your Device:

- Add a new frame.
- Choose a preset size (Desktop or Phone etc.).

2. Place Your Elements Inside the Frame:

- Add components to the frame.

3. Set Constraints on Each Element:

- Select an element inside the frame.
- In the **right-hand panel**, find the **Constraints** section.
- Set how the element should behave when the frame resizes.

4. Resize the Frame to Test Responsiveness:

- Drag the frame’s edges or change width in the right panel.
- You’ll see how elements stretch, stick, or reposition.

### References
- Chatgpt was used figuring out how to work with constraints.
- Youtube video's were also used for helping to understand how to work with constraints.

Video on how to make your figma design responsive: [Make Your Web Design Responsive in 10 Minutes | Figma Tutorial](https://www.youtube.com/watch?v=gwiX0oASlEw)

## Learning Story 187
As a student, I want to be able to make reusable components, so I can speed up my workflow and avoid repeating the same design work.

### What I have learned
I want to learn how to create reusable components in Figma to make my design process faster and more consistent. This will help me avoid repeating the same work and make updates more efficient across my designs. For this design in created a reusable navbar and buttons, so I can use them on all the pages needed and easily change all the buttons used when only changing the component itself. To figure out how to make these components I first asked chatgpt for clear instructions. After following all the steps chat gave I made the components needed for the design.

![Component](../assets/Figma/ReusableComponent.png)

### Steps to make component

1. Design an element.

2. Select the element, right-click, and choose "Create component" or press Cmd/Ctrl + Alt + K.

3. Name the component.

4. Use the component by dragging instances from the Assets panel or copy-pasting it across frames/pages.

5. When you followed all the steps above you should be able to change all copy of this component when you only make a change to the main component.

### References
- Chatgpt was used to figure out the steps on how to make components in figma.

## Learning story 195
As a student, I want to understand and implement a many-to-many relationship in our database design so that I can correctly model real-world interactions between patients and therapists.

### What I have learned
I wanted to learn how to create a junction table to represent a many-to-many relationship, so I started by creating the patient and therapist tables in MySQL Workbench. Then, using the relationship tools from the toolbar, I created a junction table called patient_has_therapist, where I linked the primary keys from both tables and set them as a composite primary key to accurately model the relationship.

![Relationship](../assets/LearningStory195.png)

### Steps to create junction table (for Many-to-Many Relationship)

1. Open Your EER Diagram.

2. Add the Two Main Tables.

- Create the tables you for the many-to-many relationship.

3. Use the Relationship Tool to Create the Junction Table.

- Select the “Many-to-Many Non-Identifying Relationship” tool from the vertical toolbar (dashed line with crow’s feet at both ends).
- Click first on the first table (e.g., patient), then on the second table (e.g., therapist).
- MySQL Workbench will automatically create a junction table (e.g., patient_has_therapist) and add the necessary foreign key relationships to both original tables.

4. Edit the Junction Table.

- Double-click the auto-created table.

**Verify**

- It has the two columns needed.
- Both are foreign keys referencing their respective tables.
- Both are part of the composite primary key (check the PK boxes).
- Check if both keys are NN (Not Null).

5. Save Your Work.

### References
- One of my team members helped me with understanding how to create the junction table.
- Chatgpt was used to help created the Steps to create junction table.