from neo4j.exceptions import ConstraintError
import drivers
from credentials import credentials
import uuid


class Communicator:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    This class contains methods necessary to interact with the Neo4j database.
    """

    def __init__(self) -> None:
        self.driver = drivers.init_driver(
            credentials["uri"],
            username=credentials["username"],
            password=credentials["password"],
        )
        self.database_name = "neo4j"

    def test_database_connection(self):
        """
        This function tests database connection.
        """

        def test(tx):
            return tx.run(
                """
                match (d)
                return d
                limit 1
                """
            ).data()

        try:
            with self.driver.session(database=self.database_name) as session:
                print("database name: ", self.database_name)
                result = session.execute_read(test)
                print("result: ", result)

                return result

        except ConstraintError as err:
            print(err)

            session.close()

    def load_media(self, media: dict, topics: list):
        """
        This function tests database connection.
        """

        def load(tx):
            return tx.run(
                """
                with $media as media
                merge (m:Media {id: media.id})
                set m.overview = media.overview, m.releaseYear = media.releaseYear,
                    m.title = media.name, m.type = media.itemType.name,
                    m.lastUpdated = datetime()
                
                with m
                unwind $topics as topic
                call {
                    with m, topic as topic
                    with m, topic,
                    case topic.noSum
                        when 0 then 0.01
                        else toFloat(topic.noSum)
                    end as noSum
                    merge (t:Topic {id: topic.TopicId, title: replace(topic.slug, '-', ' ')})
                    create (te:TriggerEvent)
                    set te.description = topic.comment, te.yesCount = topic.yesSum,
                        te.noCount = noSum, te.id = apoc.create.uuid(),
                        te.confidence = toFloat(topic.yesSum) / noSum

                    with m, t, te
                    merge (m)-[:HAS_EVENT]->(te)-[:HAS_TOPIC]->(t)
                }
    
                """,
                media=media,
                topics=topics,
            )

        try:
            with self.driver.session(database=self.database_name) as session:
                print("database name: ", self.database_name)
                result = session.execute_write(load)
                print("result: ", result)

                return result

        except ConstraintError as err:
            print(err)

            session.close()
