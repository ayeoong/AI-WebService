const body = document.querySelector('body');
    const modal = document.querySelector('.modal');
    const modalClose = document.querySelector('.modal-close');
    const btnOpenPopupList = document.querySelectorAll('.btn-open-popup');
    const modalItem = document.querySelector('.modal-items');

    btnOpenPopupList.forEach(btnOpenPopup =>
      btnOpenPopup.addEventListener('click', (e) => {
        modal.classList.toggle('show');

        if (modal.classList.contains('show')) {
          body.style.overflow = 'hidden';
        }
        var originImg = e.currentTarget.querySelector('.ori-img');
        var testImg = originImg.cloneNode(true)
        var inputText = e.currentTarget.querySelector('.input-text');
        var testText = inputText.cloneNode(true)
        var imgUser = e.currentTarget.querySelector('.img-user');
        var testUser = imgUser.cloneNode(true)

        testImg.style.display = 'block'
        testText.style.display = 'block'
        testUser.style.display = 'block'
        modalItem.children[0].appendChild(testImg)
        modalItem.children[1].appendChild(testText)
        modalItem.children[1].appendChild(testUser)
        console.log(testImg)
      })
    );

    modalClose.addEventListener('click', (event) => {
      modal.classList.toggle('show');
      while (modalItem.children[0].firstChild) {
        modalItem.children[0].removeChild(modalItem.children[0].firstChild);
      } 
      while (modalItem.children[1].firstChild) {
        modalItem.children[1].removeChild(modalItem.children[1].firstChild);
      } 
      if (!modal.classList.contains('show')) {
          body.style.overflow = 'auto';
      }
    });

    modal.addEventListener('click', (event) => {
      if (event.target === modal) {
        modal.classList.toggle('show');
        while (modalItem.children[0].firstChild) {
        modalItem.children[0].removeChild(modalItem.children[0].firstChild);
        } 
        while (modalItem.children[1].firstChild) {
          modalItem.children[1].removeChild(modalItem.children[1].firstChild);
        } 
        if (!modal.classList.contains('show')) {
            body.style.overflow = 'auto';
        }

        if (!modal.classList.contains('show')) {
          body.style.overflow = 'auto';
        }
      }
    });