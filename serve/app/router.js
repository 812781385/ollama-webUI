/**
 * @param {Egg.Application} app - egg application
 */
module.exports = app => {
  const { router, controller } = app;
  router.get('/', controller.home.index);
  router.get('/', controller.home.index);
  router.post('/chat', controller.chat.createStreamChat);
  router.post('/tags', controller.chat.getTags);
  router.post('/pull', controller.chat.pullModel);
  router.post('/delete', controller.chat.deleteModel);
  router.post('/addData', controller.chat.addDataForDB);
  router.post('/deleteCollection', controller.chat.deleteCollection);
};
