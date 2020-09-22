import time
import json
import logging
import logging.config
from importlib import import_module
from .__version__ import __version__


def load_class(module_class):
    qname = module_class.split('.')
    length = len(qname)
    clazz = qname[length-1]
    module = ""
    for i in range(length-1):
        module += qname[i] + "."

    module = module.rstrip('.')
    return getattr(import_module(module), clazz)


def main():
    """ Starts all the threads and control the status periodically. """
    logger = logging.getLogger('iotconnect')
    logging.config.fileConfig('iotconnect/logging.conf')

    logger.info('======================= Starting IOTConnect (v%s) =======================' % __version__)
    Monitors = []
    Publishers = []
    try:
        with open('iotconnect/iotconnect.config.json') as config_file:
            config = json.loads(config_file.read())
    except (FileNotFoundError):
        raise Exception('Config file not found')
    except json.decoder.JSONDecodeError as err:
        raise Exception('Error parsing config file: %s', err)

    # Load the publishers
    logger.info('=== Loading publishers ===')
    for pub_config in config['publishers']:
        try:
            logger.info('Loading publisher for class %s...',
                        pub_config['class'])
            Publisher = load_class(pub_config['class'])
            pub_instance = Publisher(pub_config)
            Publishers.append(pub_instance)
            logger.info('%s loaded', pub_instance.__class__.__name__)
        except (Exception) as err:
            logger.error('Error loading publisher for class %s. %s',
                         pub_config['class'], err)

    # Load the monitors
    logger.info('=== Loading monitors ===')
    for monitor_config in config['monitors']:
        try:
            logger.info('Loading monitor for class %s',
                        monitor_config['class'])
            Monitor = load_class(monitor_config['class'])
            monitor_instance = Monitor(monitor_config, Publishers)
            Monitors.append(monitor_instance)
            logger.info('%s loaded', monitor_instance.__class__.__name__)
        except (Exception) as err:
            logger.error('Error loading monitor for class %s. %s',
                         monitor_config['class'], err, exc_info=True)

    main_running = True
    try:
        while main_running:
            state_info = {'timestamp': int(round(time.time())),
                          'state': 'running'}
            monitors_state_info = []
            for p in Monitors:
                status = p.check_thread()
                if not status:
                    logger.error('%s not started', p.__class__.__name__)
                    try:
                        p.start()
                    except Exception as ex:
                        logger.error('Error starting %s. %s',
                                     p.__class__.__name__, ex)
                monitors_state_info.append({p.__class__.__name__: 'started' if p.check_thread() else 'stopped'})
            state_info.update({'monitors': monitors_state_info})
            for pb in Publishers:
                pb.publish('state', state_info)

            if main_running:
                # Wait some time before cheking again the monitors
                time.sleep(15)
    except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
        main_running = False
    except Exception as ex:
        main_running = False
        logger.error('Unexpected error: {}'.format(ex), exc_info=True)
    finally:
        logger.info('=== Stopping monitors ===')
        for pl in Monitors[::-1]:  # reverse monitors
            pl.stop()
        logger.info('=== Closing publishers ===')
        for pb in Publishers:
            pb.close()
        logger.info('======================= IOTConnect stopped =======================')


if __name__ == '__main__':
    main()
