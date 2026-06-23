// const allContsIMages = document.querySelectorAll(".images-post")

// allContsIMages.forEach(boxIMages => {
//     console.log(12)
//     let countImages = boxIMages.querySelectorAll("img").length
//     const allImages = boxIMages.querySelectorAll("img")

//     if (countImages > 3){
//         const massiveNumbers = []
//         while (countImages > 0){
//             if (countImages % 3 != 0){
//                 if (countImages - 3 > 0 && massiveNumbers[massiveNumbers.length - 1] != 3){
//                     massiveNumbers.push(3)
//                     countImages = countImages - 3
//                 }else if(countImages - 3 > 0 && massiveNumbers[massiveNumbers.length - 1] == 3){
//                     massiveNumbers.push(2)
//                     countImages = countImages - 2
//                 }else if(countImages - 2 > 0 && massiveNumbers[massiveNumbers.length - 1] != 2){
//                     massiveNumbers.push(2)
//                     countImages = countImages - 2
//                 }else{
//                     massiveNumbers.push(1)
//                     countImages = countImages - 1
//                 }
//             }else{
//                 massiveNumbers.push(3)
//                 countImages= countImages-3
//             }
            

//             console.log(massiveNumbers)
//         }
//     }else{
//         const width = (countImages <= 2) ? '30.1vw' : '19.69vw'
//         allImages.forEach(image => {
//             image.style.width = width
//         })
//     }
// })

const allContsIMages = document.querySelectorAll(".images-post")

allContsIMages.forEach(boxIMages => {
    let countImages = boxIMages.querySelectorAll("img").length
    const allImages = boxIMages.querySelectorAll("img")

    if (countImages > 3) {
        const massiveNumbers = []
        
        if (countImages === 4) {
            massiveNumbers.push(3, 1)
        } 

        else if (countImages % 3 == 1) {
            massiveNumbers.push(2) 
            let remaining = countImages - 4 
            
            while (remaining > 0) {
                massiveNumbers.push(3)
                remaining -= 3
            }
            massiveNumbers.push(2)
        } 
        else {
            let tempCount = countImages
            let wantThree = true 
            
            while (tempCount > 0) {
                let target = (tempCount === 2) ? 2 : (wantThree ? 3 : 2)
                massiveNumbers.push(target)
                tempCount -= target
                wantThree = !wantThree 
            }
        }
    
        console.log(massiveNumbers)

    } else {
        const width = (countImages <= 2) ? '30.1vw' : '19.69vw'
        allImages.forEach(image => {
            image.style.width = width
        })
    }
})